from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from .models import Product, Order, OrderItem
from .forms import RegisterForm, CheckoutForm

def home(request):
    products = Product.objects.filter(is_active=True)
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, "store/home.html", {"products": products, "query": query})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})

def _cart_products(request):
    cart = request.session.get("cart", {})
    products, total = [], Decimal("0.00")
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id), is_active=True)
            quantity = max(1, int(quantity))
            subtotal = product.price * quantity
            products.append({"product": product, "quantity": quantity, "subtotal": subtotal})
            total += subtotal
        except (Product.DoesNotExist, ValueError, TypeError):
            continue
    return products, total

def cart_detail(request):
    products, total = _cart_products(request)
    return render(request, "store/cart.html", {"items": products, "total": total})

def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = request.session.get("cart", {})
    current = int(cart.get(str(product_id), 0))
    if current < product.stock:
        cart[str(product_id)] = current + 1
        request.session["cart"] = cart
        messages.success(request, f"{product.name} added to your cart.")
    else:
        messages.warning(request, "Sorry, there is not enough stock.")
    return redirect(request.POST.get("next") or "cart")

def update_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        try:
            quantity = int(request.POST.get("quantity", 1))
            product = get_object_or_404(Product, pk=product_id)
            if quantity <= 0:
                cart.pop(str(product_id), None)
            elif quantity <= product.stock:
                cart[str(product_id)] = quantity
            else:
                messages.warning(request, f"Only {product.stock} items are available.")
            request.session["cart"] = cart
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid quantity.")
    return redirect("cart")

def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        cart.pop(str(product_id), None)
        request.session["cart"] = cart
        messages.info(request, "Item removed from cart.")
    return redirect("cart")

@login_required
def checkout(request):
    items, total = _cart_products(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("home")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Re-check stock at order time to avoid overselling.
                for item in items:
                    product = Product.objects.select_for_update().get(pk=item["product"].pk)
                    if product.stock < item["quantity"]:
                        messages.error(request, f"Not enough stock for {product.name}. Please update your cart.")
                        return redirect("cart")
                order = Order.objects.create(
                    user=request.user, full_name=form.cleaned_data["full_name"],
                    email=form.cleaned_data["email"], address=form.cleaned_data["address"],
                    phone=form.cleaned_data["phone"], total=total,
                )
                for item in items:
                    product = Product.objects.get(pk=item["product"].pk)
                    OrderItem.objects.create(order=order, product=product,
                        product_name=product.name, price=product.price, quantity=item["quantity"])
                    product.stock -= item["quantity"]
                    product.save(update_fields=["stock"])
            request.session["cart"] = {}
            return redirect("order_success", order_id=order.pk)
    else:
        form = CheckoutForm(initial={"full_name": request.user.get_full_name(), "email": request.user.email})
    return render(request, "store/checkout.html", {"form": form, "items": items, "total": total})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "store/order_success.html", {"order": order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "store/order_history.html", {"orders": orders})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "store/register.html", {"form": form})

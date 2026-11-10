def cart_count(request):
    cart = request.session.get("cart", {})
    return {"cart_count": sum(int(qty) for qty in cart.values())}

from django.core.management.base import BaseCommand
from store.models import Product

SAMPLES = [
    ("Everyday Backpack", "A durable everyday backpack with a padded laptop sleeve.", "1499.00", "Accessories", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800", 18),
    ("Wireless Headphones", "Comfortable over-ear headphones for music and calls.", "2299.00", "Electronics", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800", 14),
    ("Classic Sneakers", "Minimal sneakers designed for daily comfort.", "1899.00", "Fashion", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800", 20),
    ("Smart Watch", "A sleek smart watch for everyday activity tracking.", "3199.00", "Electronics", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800", 10),
    ("Ceramic Coffee Mug", "A clean, modern ceramic mug for your morning coffee.", "399.00", "Home", "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=800", 30),
    ("Sunglasses", "Lightweight sunglasses with a timeless frame.", "799.00", "Accessories", "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800", 16),
]

class Command(BaseCommand):
    help = "Create sample products for the demo store"

    def handle(self, *args, **options):
        for name, description, price, category, image_url, stock in SAMPLES:
            Product.objects.update_or_create(
                name=name,
                defaults={"description": description, "price": price, "category": category,
                          "image_url": image_url, "stock": stock, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(SAMPLES)} sample products."))

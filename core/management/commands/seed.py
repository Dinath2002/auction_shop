from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import Category, Product
from auctions.models import Listing
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='seller').exists():
            User.objects.create_user('seller', password='seller123')
        seller = User.objects.get(username='seller')

        cat, _ = Category.objects.get_or_create(name='Electronics', slug='electronics')
        for title, price in [('Headphones', 6500), ('Keyboard', 7200), ('GPU Stand', 3500)]:
            p, _ = Product.objects.get_or_create(
                category=cat, title=title, slug=slugify(title),
                defaults={'price': price, 'stock': 10}
            )
            Listing.objects.get_or_create(
                product=p, seller=seller, starting_price=price*0.8,
                buy_now_price=price*1.2,
                starts_at=timezone.now(), ends_at=timezone.now()+timedelta(days=3)
            )
        self.stdout.write(self.style.SUCCESS('Seeded!'))

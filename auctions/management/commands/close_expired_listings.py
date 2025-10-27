from django.core.management.base import BaseCommand
from django.utils import timezone
from auctions.models import Listing

class Command(BaseCommand):
    help = 'Close auctions whose end time has passed.'

    def handle(self, *args, **kwargs):
        qs = Listing.objects.filter(is_closed=False, ends_at__lte=timezone.now())
        count = 0
        for l in qs:
            l.is_closed = True
            l.save(update_fields=['is_closed'])
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Closed {count} expired listings.'))

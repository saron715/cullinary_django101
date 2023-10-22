from django.core.management.base import BaseCommand
from cook.models import CuisineType, Community

class Command(BaseCommand):
    help = 'Pre-create communities for each cuisine type'

    def handle(self, *args, **options):
        cuisine_types = CuisineType.objects.all()

        for cuisine_type in cuisine_types:
            Community.objects.get_or_create(
                cuisine_type=cuisine_type,
                name=cuisine_type.name,
                description=f"A community for {cuisine_type.name} enthusiasts."
            )

        self.stdout.write(self.style.SUCCESS('Pre-created communities for all cuisine types'))

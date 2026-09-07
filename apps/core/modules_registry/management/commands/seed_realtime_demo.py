from django.core.management.base import BaseCommand, CommandError

from apps.core.modules_registry.bootstrap import RegistryBootstrapService



class Command(BaseCommand):
    help = "Seeds the database with demo data for real-time features."

    def handle(self, *args, **options):
        try:
            RegistryBootstrapService.bootstrap(include_entity_types=True)
            self.stdout.write(self.style.SUCCESS("Successfully seeded real-time demo data."))
        except Exception as e:
            raise CommandError(f"Error seeding real-time demo data: {e}")


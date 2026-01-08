from django.core.management.base import BaseCommand
from modules.examples.seeder import ExampleSeeder

class Command(BaseCommand):

    def handle(self, *args, **options):
        seeder = ExampleSeeder(count=200)
        seeder.clear()
        seeder.run()
        self.stdout.write(self.style.SUCCESS('Successfully seeded ExampleModel'))
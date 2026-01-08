from .models import ExampleModel
from faker import Faker

class ExampleSeeder:

    def __init__(self, count=10):
        self.count = count
        self.fake = Faker()

    def run(self):
        for _ in range(self.count):
            ExampleModel.objects.create(
                name=self.fake.name(),
                address=self.fake.address(),
                note=self.fake.text()
            )
    
    def clear(self):
        ExampleModel.objects.all().delete()
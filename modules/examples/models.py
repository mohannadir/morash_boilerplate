from django.db import models

class ExampleModel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    note = models.TextField()

    def __str__(self):
        return self.name
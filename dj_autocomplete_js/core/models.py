from django.db import models

# Create your models here.


class FakeAdress(models.Model):
    address = models.TextField()

    def __str__(self) -> str:
        return self.address

from django.db import models


class Prefix(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    prefix = models.ForeignKey(Prefix, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

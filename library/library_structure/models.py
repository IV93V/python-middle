from django.db import models
from person.models import Librariers


class Halls(models.Model):
    name = models.CharField(max_length=100)
    librarer = models.ForeignKey(Librariers, on_delete=models.CASCADE)

    class Meta:
        db_table = "Halls"
        verbose_name = "Залы библиотеки"


class Racks(models.Model):
    number = models.CharField(max_length=10)
    hall = models.ForeignKey(Halls, on_delete=models.CASCADE)

    class Meta:
        db_table = "Racks"
        verbose_name = "Стеллажи"
        unique_together = (("number", "hall"),)


class Shelf(models.Model):
    number = models.CharField(max_length=10)
    rack = models.ForeignKey(Racks, on_delete=models.CASCADE)

    class Meta:
        db_table = "Shelf"
        verbose_name = "Полки"
        unique_together = (("number", "rack"),)

from django.db import models
from person.models import Agents
from books.models import Books

class ReaderCards(models.Model):
    agent = models.ForeignKey(Agents, on_delete=models.CASCADE, unique=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    date_take = models.DateField()
    date_return = models.DateField(blank=True)

    class Meta:
        db_table = 'ReaderCards'
        verbose_name = 'Карточки читателей'

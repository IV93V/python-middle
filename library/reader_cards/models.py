from django.db import models
from person.models import Agents
from books.models import Books

class ReaderCards(models.Model):
    agent = models.ForeignKey(Agents, on_delete=models.CASCADE, unique=True)
    #book = models.ForeignKey(ReaderCardBook, on_delete=models.CASCADE, related_name='books')
    #reading_place = models.CharField(max_length=10, choices=READING_PLACE)

    class Meta:
        db_table = 'ReaderCards'
        verbose_name = 'Карточки читателей'

class ReaderCardBook(models.Model):
    READING_PLACE = (
        (1, 'На руки'),
        (2, 'Для чтения в зале'),
    )
    readercards = models.ForeignKey(ReaderCards, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    give_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    reading_place = models.SmallIntegerField(choices=READING_PLACE)
    class Meta:
        db_table = 'ReaderCards_book'
        verbose_name = 'Книги в карточке читателя'
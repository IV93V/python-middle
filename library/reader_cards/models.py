from django.db import models
from django.utils import timezone
from datetime import timedelta
from person.models import Agents
from books.models import Books


class OutOfTerms(models.Manager):
    def get_queryset(self):
        days_limit = timezone.now() - timedelta(days=30)
        return (
            super()
            .get_queryset()
            .filter(return_date__isnull=True, give_date__lte=days_limit)
        )


class ReaderCards(models.Model):
    agent = models.ForeignKey(Agents, on_delete=models.CASCADE, unique=True)
    def __str__(self):
        agt = Agents.__str__(self.agent)
        return 'Карточка читателя '+agt
    # book = models.ForeignKey(ReaderCardBook, on_delete=models.CASCADE, related_name='books')
    # reading_place = models.CharField(max_length=10, choices=READING_PLACE)

    class Meta:
        db_table = "ReaderCards"
        verbose_name = "Карточки читателей"


class ReaderCardBook(models.Model):
    READING_PLACE = (
        (1, "На руки"),
        (2, "Для чтения в зале"),
    )
    objects = models.Manager()
    out_of_terms = OutOfTerms()
    readercards = models.ForeignKey(ReaderCards, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    give_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    reading_place = models.SmallIntegerField(choices=READING_PLACE)

    class Meta:
        db_table = "ReaderCards_book"
        verbose_name = "Книги в карточке читателя"

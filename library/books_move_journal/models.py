from django.db import models
from library_structure.models import Shelf
from books.models import Books
from person.models import Librariers
from reader_cards.models import ReaderCards


class BooksMoveJournal(models.Model):
    book = models.ForeignKey(Books, on_delete = models.CASCADE)
    move_date = models.DateField()
    moved_librarier = models.ForeignKey(Librariers, on_delete = models.CASCADE)
    shelf_prev = models.ForeignKey(Shelf, on_delete = models.CASCADE, related_name='shelf_prev', blank=True, null=True)
    shelf_new = models.ForeignKey(Shelf, on_delete=models.CASCADE, related_name='shelf_new', blank=True, null=True)
    reader_prev = models.ForeignKey(ReaderCards, on_delete = models.CASCADE, related_name='reader_prev', blank=True, null=True)
    reader_new = models.ForeignKey(ReaderCards, on_delete = models.CASCADE, related_name='reader_new', blank=True, null=True)

    class Meta:
        db_table = 'BooksMoveJournal'
        verbose_name = 'Журнал перемещения книг'

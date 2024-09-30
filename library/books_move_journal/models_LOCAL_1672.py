import copy
from django.utils import timezone
from datetime import timedelta
from django.db import models
from library_structure.models import Shelf
from books.models import Books
from person.models import Librariers, Agents
from reader_cards.models import ReaderCards, ReaderCardBook


class UnitNotFound(Exception):
    pass


class ReaderError(Exception):
    pass


class OccupiedShelf(Exception):
    pass


class ThirtyDays(models.Manager):
    def get_queryset(self):
        days_limit = timezone.now() - timedelta(days=30)
        return super().get_queryset().filter(move_date__gte=days_limit)


class BooksMoveJournal(models.Model):
    objects = models.Manager()
    thirty_days = ThirtyDays()
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    move_date = models.DateField()
    moved_librarier = models.ForeignKey(Librariers, on_delete=models.CASCADE)
    shelf_prev = models.ForeignKey(
        Shelf,
        on_delete=models.SET_NULL,
        related_name="shelf_prev",
        blank=True,
        null=True,
    )
    shelf_new = models.ForeignKey(
        Shelf,
        on_delete=models.SET_NULL,
        related_name="shelf_new",
        blank=True,
        null=True,
    )
    reader_prev = models.ForeignKey(
        ReaderCards,
        on_delete=models.SET_NULL,
        related_name="reader_prev",
        blank=True,
        null=True,
    )
    reader_new = models.ForeignKey(
        ReaderCards,
        on_delete=models.SET_NULL,
        related_name="reader_new",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "BooksMoveJournal"
        verbose_name = "Журнал перемещения книг"


def GiveBookToReader(book_name, date, reader_card, place, librarier):
    # Выдача книги
    # book_number - номер книги
    # date        - дата выдачи
    # reader_card - id карты читателя
    # place       - выдача книг в зал (2) или на дом (1)
    # librarier   - id библиотекаря
    book_instance = Books.objects.filter(name=book_name, shelf__isnull=False).first()
    reader_book_count_check = ReaderCardBook.objects.filter(
        readercards=reader_card, return_date__isnull=True
    ).count()
    if reader_book_count_check >= 3:
        raise ReaderError(
            "У читателя на руках 3 или более книг. Выдача новых книг запрещена"
        )
    if not book_instance:
        raise UnitNotFound("Такой книги нет на полках")
    else:
        journal_add_record = BooksMoveJournal(
            book=book_instance,
            move_date=date,
            moved_librarier=Librariers.objects.get(pk=librarier),
            shelf_prev=Shelf.objects.get(pk=getattr(book_instance, "shelf").id),
            shelf_new=None,
            reader_prev=None,
            reader_new=ReaderCards.objects.get(pk=reader_card),
        )
        reader_card_book_add = ReaderCardBook(
            readercards_id=reader_card,
            book_id=book_instance.id,
            give_date=date,
            return_date=None,
            reading_place=place,
        )
        Books.objects.filter(id=book_instance.id).update(shelf=None)
        journal_add_record.save()
        reader_card_book_add.save()


def GetBookFromReader(book_number, date, reader_card, shelf, librarier):
    # Возврат книги
    # book_number - номер книги
    # date        - дата возврата
    # reader_card - id карты читателя
    # shelf       - id полки, на которую убираем книгу. Может быть None
    # librarier   - id библиотекаря
    book_instance = Books.objects.get(book_number=book_number)
    if shelf == None:
        occupied_shelfs = Books.objects.filter(shelf__isnull=False).values("shelf")
        shelf = Shelf.objects.exclude(pk__in=occupied_shelfs).first()
        if not shelf:
            raise OccupiedShelf("Свободных полок не найдено")
    else:
        shelf_occupied_check = Books.objects.get(shelf=shelf)
        if shelf_occupied_check:
            raise OccupiedShelf("Указанная полка уже занята")
    journal_add_record = BooksMoveJournal(
        book=book_instance,
        move_date=date,
        moved_librarier=Librariers.objects.get(pk=librarier),
        shelf_prev=None,
        shelf_new=shelf,
        reader_prev=ReaderCards.objects.get(pk=reader_card),
        reader_new=None,
    )
    ReaderCardBook.objects.filter(
        book_id=book_instance.id, readercards=reader_card, return_date__isnull=True
    ).update(return_date=date)
    Books.objects.filter(id=book_instance.id).update(shelf=shelf)
    journal_add_record.save()


def MoveBookToShelf(book_number, date, shelf, librarier, is_sort_operation):
    # Перемещение книг с полки на полку
    # book_number - номер книги
    # date        - дата перемещения
    # shelf       - id полки, на которую убираем книгу. Может быть None
    # librarier   - id библиотекаря
    # is_sort_operation - True, если делаем сортировку книг - предварительно очищаем данные о расположении книг на полках
    try:
        if is_sort_operation == True:
            book_instance = Books.objects.get(book_number=book_number)
        else:
            book_instance = Books.objects.get(
                book_number=book_number, shelf__isnull=False
            )
    except UnitNotFound:
        print("Книга не найдена")
    shelf_instance = Shelf.objects.get(pk=shelf)
    shelf_occupied_check = Books.objects.filter(shelf=shelf)
    if shelf_occupied_check:
        raise OccupiedShelf("Указанная полка уже занята")

    Books.objects.filter(id=book_instance.id).update(shelf=shelf_instance.id)
    journal_add_record = BooksMoveJournal(
        book=book_instance,
        move_date=date,
        moved_librarier=Librariers.objects.get(pk=librarier),
        shelf_prev=book_instance.shelf,
        shelf_new=shelf_instance,
        reader_prev=None,
        reader_new=None,
    )
    journal_add_record.save()


def SortBooks(librarier, date):
    # Сортировка книг
    # librarier   - id библиотекаря
    # date        - дата перемещения
    books_list = Books.objects.filter(shelf__isnull=False).order_by(
        "edition_kind", "name", "edition_date__year", "pages_count"
    )
    books_list_to_sort_tmp = list(books_list.values_list("id", "shelf"))
    books_list_to_sort = copy.deepcopy(books_list_to_sort_tmp)
    books_list.update(shelf=None)
    for i, book in enumerate(books_list_to_sort):
        i = i + 1
        book_instance = Books.objects.get(pk=book[0])
        shelf_instance = Shelf.objects.get(pk=i)
        MoveBookToShelf(book_instance.book_number, date, shelf_instance.id, librarier)

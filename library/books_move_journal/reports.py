from django.db.models import (
    OuterRef,
    Subquery,
    Count,
    Avg,
    OuterRef,
    Subquery,
    CharField,
    Value as V,
)
from django.contrib.postgres.aggregates import ArrayAgg, StringAgg
from django.db.models.functions import Concat, Cast
from books.models import EditionKinds
from library_structure.models import *
from reader_cards.models import *
from reader_cards.models import ReaderCardBook
from books_move_journal.models import BooksMoveJournal


def ReportBooksOfAuthor(author):
    # Количество книг определенного автора в библиотеке
    return Books.objects.filter(author__books=author).count()


def ReportTopBooks():
    # 10 самых популярных книг за последний месяц
    return list(
        BooksMoveJournal.thirty_days.values("book__name")
        .annotate(book_count=Count("book"))
        .order_by("-book_count")[:10]
    )


def ReportGivenBooks():
    # Количество книг, которые сейчас находятся на руках в разрезе читателей
    return list(
        ReaderCardBook.objects.filter(return_date__isnull=True)
        .values(
            "readercards__agent__surname",
            "readercards__agent__firstname",
            "readercards__agent__lastname",
        )
        .annotate(Count("book"))
    )


def ReadersOutOfTerms():
    # Перечень читателей, которые просрочили возврат книг
    return list(
        ReaderCardBook.out_of_terms.values(
            "readercards__agent__surname",
            "readercards__agent__firstname",
            "readercards__agent__lastname",
        )
    )


def ReportTopActiveReaders():
    # 10 самых активных читателей, которые взяли больше всего книг, за прошедший месяц
    return list(
        BooksMoveJournal.thirty_days.filter(reader_new__isnull=False)
        .values(
            "reader_new__agent__surname",
            "reader_new__agent__firstname",
            "reader_new__agent__lastname",
        )
        .annotate(book_count=Count("book"))
        .order_by("-book_count")[:10]
    )


def ReportAveragePages():
    # Среднее количество страниц в разрезе видов изданий, которые прочитали читатели за последний месяц
    return list(
        Books.objects.values("edition_kind__edition_type").annotate(Avg("pages_count"))
    )


def ReportTopMovedBooks():
    # 10 самых перемещаемых книг за последний месяц
    return list(
        BooksMoveJournal.thirty_days.filter(
            shelf_prev__isnull=False, shelf_new__isnull=False
        )
        .values("book__name")
        .annotate(book_count=Count("book"))
        .order_by("-book_count")[:10]
    )


def PrintLibraryStructure():
    # список всех залов с наименованием всех связанных стеллажей и полок
    shelf_numbers_subquery = Subquery(
        Shelf.objects.filter(rack_id=OuterRef("id"))
        .values("rack_id")
        .annotate(shelfs=StringAgg("number", delimiter=", "))
        .values("shelfs")
    )

    racks = (
        Racks.objects.annotate(shelfs=(shelf_numbers_subquery))
        .annotate(rack_shelfs=Concat(V("Стеллаж "), "number", V(", полки: "), "shelfs"))
        .values()
    )

    racks_numbers_subquery = Subquery(
        racks.filter(hall_id=OuterRef("id"))
        .values("hall_id")
        .annotate(hall_racks=StringAgg("rack_shelfs", delimiter=", "))
        .values("hall_racks")
    )

    halls = (
        Halls.objects.annotate(h_racks=(racks_numbers_subquery))
        .annotate(hall_rack_shelfs=Concat(V("Зал: "), "name", V(": "), "h_racks"))
        .values("hall_rack_shelfs")
    )

    return list(halls)


def EditionKindsBooks():
    # список всех типов публикаций, каждая из них должна содержать наименование книг, которые ни разу не брали читать
    books_taken = (
        ReaderCardBook.objects.values("book__name").distinct().order_by("book__name")
    )
    books_tmp = (
        Books.objects.exclude(name__in=books_taken)
        .values("edition_kind")
        .annotate(names=StringAgg("name", delimiter=", "))
    )

    book_names_subquery = Subquery(
        books_tmp.filter(edition_kind=OuterRef("id")).values("names")
    )

    eks = (
        EditionKinds.objects.annotate(ek_books=(book_names_subquery))
        .annotate(
            ek_book_agg=Concat(
                V("Издание: "), "edition_type", V(", Книги: "), "ek_books"
            )
        )
        .values("ek_book_agg")
    )

    return eks


def BookMovingHistory(order):
    # список всех книг, у каждой из книг должна быть история перемещения между полками с наименованием каждой из них: один атрибут - полки в алфавитном порядке, второй атрибут - в хронологическом.
    # order == True  - сортировка по дате,
    # order == False - сортировка по полкам в алфавитном порядке
    if order == True:
        books_history_tmp_ordered = (
            BooksMoveJournal.objects.filter(
                shelf_prev__isnull=False, shelf_new__isnull=False
            )
            .values("book", "move_date")
            .annotate(
                rack_shelf=Concat(
                    V("Стеллаж: "),
                    "shelf_new__rack__number",
                    V(", полка: "),
                    "shelf_new__number",
                )
            )
            .annotate(move_date_formatted=Cast("move_date", CharField()))
            .order_by("move_date")
        )
    else:
        books_history_tmp_ordered = (
            BooksMoveJournal.objects.filter(
                shelf_prev__isnull=False, shelf_new__isnull=False
            )
            .values("book", "move_date")
            .annotate(
                rack_shelf=Concat(
                    V("Стеллаж: "),
                    "shelf_new__rack__number",
                    V(", полка: "),
                    "shelf_new__number",
                )
            )
            .annotate(move_date_formatted=Cast("move_date", CharField()))
            .order_by("rack_shelf")
        )

    books_history_tmp = books_history_tmp_ordered.values("book").annotate(
        history=Concat("move_date_formatted", V(" перемещена на "), "rack_shelf")
    )

    books_history_tmp_aggregated = books_history_tmp.values("book").annotate(
        history_aggregated=StringAgg("history", delimiter=", ")
    )

    books_history_subquery = books_history_tmp_aggregated.filter(
        book=OuterRef("id")
    ).values("history_aggregated")

    books_history = (
        Books.objects.annotate(books_history=(books_history_subquery))
        .annotate(
            books_history_agg=Concat(V("Книга: "), "name", V(": "), "books_history")
        )
        .values("books_history_agg")
    )

    return books_history

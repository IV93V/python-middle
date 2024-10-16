from rest_framework import serializers
from books.models import *
from person.models import *
from library_structure.models import *
from reader_cards.models import *
from books_move_journal.models import *


class HallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Halls
        fields = ["name", "librarer"]


class RacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Racks
        fields = ["number", "hall"]


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ["number", "rack"]


class EditionKindsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditionKinds
        fields = ["edition_type"]


class AgentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agents
        fields = ["surname", "firstname", "lastname", "birth_date", "sex"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ["pid", "rating"]


class LibrarierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librariers
        fields = ["agent", "employment_date", "dismiss_date"]


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Books
        fields = [
            "name",
            "author",
            "edition_kind",
            "book_number",
            "pages_count",
            "edition_date",
            "note",
            "shelf",
        ]


class ReaderCardsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReaderCards
        fields = ["agent"]


class ReaderCardBooksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReaderCardBook
        fields = ["readercards", "book", "give_date", "return_date", "reading_place"]


class BookMoveJournalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BooksMoveJournal
        fields = [
            "book",
            "move_date",
            "moved_librarier",
            "shelf_prev",
            "shelf_new",
            "reader_prev",
            "reader_new",
        ]

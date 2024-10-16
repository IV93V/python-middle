from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from books_move_journal.models import *
from library.serializers import BookMoveJournalSerializer

class BookMoveJournalViewSet(viewsets.ModelViewSet):
    queryset = BooksMoveJournal.objects.all()
    serializer_class = BookMoveJournalSerializer
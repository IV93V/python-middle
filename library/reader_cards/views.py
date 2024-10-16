from rest_framework import viewsets
from reader_cards.models import *
from library.serializers import ReaderCardBooksSerializer, ReaderCardsSerializer

class ReaderCardsViewSet(viewsets.ModelViewSet):
    queryset = ReaderCards.objects.all()
    serializer_class = ReaderCardsSerializer

class ReaderCardBooksViewSet(viewsets.ModelViewSet):
    queryset = ReaderCardBook.objects.all()
    serializer_class = ReaderCardBooksSerializer
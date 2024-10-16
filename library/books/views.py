from rest_framework import viewsets
from books.models import *
from library.serializers import EditionKindsSerializer, BookSerializer

class EditionKindsViewSet(viewsets.ModelViewSet):
    queryset = EditionKinds.objects.all()
    serializer_class = EditionKindsSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

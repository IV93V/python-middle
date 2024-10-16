from rest_framework import viewsets
from person.models import *
from library.serializers import AgentsSerializer, AuthorSerializer, LibrarierSerializer


class AgentsViewSet(viewsets.ModelViewSet):
    queryset = Agents.objects.all()
    serializer_class = AgentsSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer

class LibrarierViewSet(viewsets.ModelViewSet):
    queryset = Librariers.objects.all()
    serializer_class = LibrarierSerializer
from rest_framework import viewsets
from library_structure.models import *
from library.serializers import HallsSerializer, RacksSerializer, ShelfSerializer

class HallsViewSet(viewsets.ModelViewSet):
    queryset = Halls.objects.all()
    serializer_class = HallsSerializer

class RacksViewSet(viewsets.ModelViewSet):
    queryset = Racks.objects.all()
    serializer_class = RacksSerializer

class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
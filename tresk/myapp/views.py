from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import GalerySerializer, ShowSerializer
from .models import Galery, Show
from django.utils import timezone
from rest_framework import viewsets

class GaleryViewSet(ModelViewSet):
    queryset = Galery.objects.all()
    serializer_class = GalerySerializer

class ShowViewSet(ModelViewSet):
    serializer_class = ShowSerializer

    def get_queryset(self):
        return Show.objects.filter(start_at__gte = timezone.now()).order_by("start_at")
    

class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
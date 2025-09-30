from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import GalerySerializer, ShowSerializer
from .models import Galery, Show

class GaleryViewSet(ModelViewSet):
    queryset = Galery.objects.all()
    serializer_class = GalerySerializer

class ShowViewSet(ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    ordering = ['start_at']
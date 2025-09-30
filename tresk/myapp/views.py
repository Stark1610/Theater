from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import GalerySerializer
from .models import Galery

class GaleryViewSet(ModelViewSet):
    queryset = Galery.objects.all()
    serializer_class = GalerySerializer


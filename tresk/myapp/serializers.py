from .models import Galery
from rest_framework import serializers

class GalerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Galery
        fields = ['id', 'photo']


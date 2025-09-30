from .models import Galery, Show
from rest_framework import serializers

class GalerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Galery
        fields = ['id', 'photo']

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id','title', 'description', 'photo', 'start_at', 'end_at', 'places']
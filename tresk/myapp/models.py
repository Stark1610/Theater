from django.db import models
from django.utils.translation import gettext_lazy as _

class Galery(models.Model):
    photo = models.ImageField(upload_to="galery/")

    def __str__(self):
        return f'{self.id}'

class Show(models.Model):
    title = models.CharField(_('title'), max_length=30, unique=True)
    description = models.TextField(_('description'))
    photo = models.ImageField(upload_to="show/", blank=True, null=True)
    start_at = models.DateTimeField()
    end_at = models.TimeField()
    places = models.IntegerField()
    
    def __str__(self):
        return f'{self.title} {self.start_at.strftime("%d/%m/%Y, %H:%M:%S")}'
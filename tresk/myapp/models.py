from django.db import models

class Galery(models.Model):
    photo = models.ImageField(upload_to="galery/")

    def __str__(self):
        return f'{self.id}'

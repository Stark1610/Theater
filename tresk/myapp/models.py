from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Galery(models.Model):
    photo = models.ImageField(upload_to="galery/")
    name = models.CharField( max_length=50)

    def __str__(self):
        return f'{self.id}'

class Show(models.Model):
    title = models.CharField(_('title'), max_length=30, unique=True)
    description = models.TextField(_('description'))
    photo = models.ImageField(upload_to="show/", blank=True, null=True)
    start_at = models.DateTimeField()
    end_at = models.TimeField()
    
    def __str__(self):
        return f'{self.title} {self.start_at.strftime("%d/%m/%Y, %H:%M:%S")}'


class TypeTicket(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='types')
    type = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    rows = models.PositiveIntegerField()
    seats_in_rows = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.show.title} - {self.type} - {self.price}Kc'
    
    class Meta:
        unique_together = ('show', 'type')

    def capacity(self):
        return self.rows * self.seats_in_rows


class Ticket(models.Model):
    type = models.ForeignKey(TypeTicket, on_delete=models.CASCADE, related_name='tickets')
    row = models.PositiveIntegerField()
    place = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "row", "place"], name="unique_seat_per_type"
            )
        ]

    def __str__(self):
        return f'{self.type.show.title} - {self.type.type} - Row: {self.row}, Place: {self.place}'

    def clean(self):
        if self.row > self.type.rows:
            raise ValidationError({'row': 'Ряд превышает максимальное количество рядов для данного типа билета.'})
        if self.place > self.type.seats_in_rows:
            raise ValidationError({'place': 'Место превышает максимальное количество мест в ряду для данного типа билета.'})

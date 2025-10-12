from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Gallery(models.Model):
    photo = models.ImageField(upload_to="gallery/")
    name = models.CharField( max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Show(models.Model):
    title = models.CharField(_('title'), max_length=30, unique=True)
    description = models.TextField(_('description'))
    photo = models.ImageField(upload_to="show/", blank=True, null=True)
    start_at = models.DateTimeField()
    end_at = models.TimeField()
    city = models.CharField(max_length=20, blank=True, null=True)
    adress = models.CharField(max_length=40, blank=True, null=True)
    
    def __str__(self):
        return f'{self.title} {self.start_at.strftime("%d/%m/%Y, %H:%M:%S")}'


class TypeTicket(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='types')
    type_ticket = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    rows = models.PositiveIntegerField()
    seats_in_rows = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.show.title} - {self.type_ticket} - {self.price}Kc'
    
    class Meta:
        unique_together = ('show', 'type_ticket')

    def capacity(self):
        return self.rows * self.seats_in_rows


class Order(models.Model):
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Заказ({self.id}) - {self.email}'


class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    type_ticket = models.ForeignKey(TypeTicket, on_delete=models.CASCADE, related_name='tickets')
    row = models.PositiveIntegerField()
    place = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type_ticket", "row", "place"], name="unique_seat_per_type"
            )
        ]

    def __str__(self):
        return f'{self.type_ticket.show.title} - {self.type_ticket.type_ticket} - Row: {self.row}, Place: {self.place}'

    def clean(self):
        if self.row > self.type_ticket.rows:
            raise ValidationError({'row': 'Ряд превышает максимальное количество рядов для данного типа билета.'})
        if self.place > self.type_ticket.seats_in_rows:
            raise ValidationError({'place': 'Место превышает максимальное количество мест в ряду для данного типа билета.'})
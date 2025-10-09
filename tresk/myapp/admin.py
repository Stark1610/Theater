from django.contrib import admin
from myapp.models import Gallery, Show, TypeTicket, Ticket, Order

admin.site.register(Gallery)
admin.site.register(Show)
admin.site.register(TypeTicket)
admin.site.register(Ticket)
admin.site.register(Order)

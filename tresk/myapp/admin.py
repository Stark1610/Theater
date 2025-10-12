from django.contrib import admin
from myapp.models import Gallery, Show, TypeTicket, Ticket, Order

class AdminShow(admin.ModelAdmin):
    search_fields = ["title"]
    ordering = ["start_at"]
    
admin.site.register(Gallery)
admin.site.register(Show, AdminShow)
admin.site.register(TypeTicket)
admin.site.register(Ticket)
admin.site.register(Order)
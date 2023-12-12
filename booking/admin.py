from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Airline)
admin.site.register(Trip_Round)
admin.site.register(Flight_Class)
admin.site.register(Offer)
admin.site.register(Location)
admin.site.register(Booking)
admin.site.register(Checkout)
admin.site.register(Flight_Status)
admin.site.register(Ticket)



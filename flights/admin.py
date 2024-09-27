from django.contrib import admin
from .models import *

admin.site.register(FlightUser)
admin.site.register(Flight)
admin.site.register(Ticket)


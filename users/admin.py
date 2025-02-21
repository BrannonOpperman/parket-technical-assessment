from django.contrib import admin
from .models import ParkingUser

class ParkingUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'license_plate', 'client')
    list_filter = ('client',)
    search_fields = ('first_name', 'last_name', 'email', 'license_plate')

admin.site.register(ParkingUser, ParkingUserAdmin)

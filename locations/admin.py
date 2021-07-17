from django.contrib import admin
from .models import *

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'availabilities', 'state', 'postal', 'id',]

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'state', 'zipcode',]

@admin.register(Geocode)
class GeocodeAdmin(admin.ModelAdmin):
    list_display = ['zipcode', 'latitude', 'longitude',]
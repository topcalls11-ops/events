from django.contrib import admin
from .models import Event, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ['title', 'college', 'category', 'date', 'approved', 'created_by']
    list_filter   = ['category', 'approved', 'date']
    search_fields = ['title', 'college', 'description']
    list_editable = ['approved']
    ordering      = ['-created_at']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'phone', 'event', 'registered_at']
    search_fields = ['name', 'email', 'event__title']
    ordering      = ['-registered_at']
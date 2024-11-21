from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'start_date', 'start_time', 'created_at')
    list_filter = ('start_date','location')
    search_fields = ('name', 'description', 'location')

admin.site.register(Event, EventAdmin)
from django.contrib import admin

# Register your models here.
from .models import Executive


class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'email', 'phone')  # Fields to display in the list view
    list_filter = ('designation',)  # Add filters for designation
    search_fields = ('name', 'email')  # Enable search by name and email


admin.site.register(Executive, ExecutiveAdmin)
from django.contrib import admin
from .models import Mentor


class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'email', 'phone', 'expertise')  # Fields to display in the list view
    search_fields = ('name', 'email', 'designation')  # Fields that can be searched
    list_filter = ('designation', 'expertise')  # Filters to use on the list view

    # Optional: You can also customize the form to be displayed when adding or editing a mentor
    fields = ('name', 'designation', 'expertise', 'email', 'phone', 'photo', 'bio')  # Form fields to display
    readonly_fields = ('email',)  # Make the email field read-only, if desired

admin.site.register(Mentor,MentorAdmin)
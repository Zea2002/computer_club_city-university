from django.contrib import admin
from .models import Alumni

class AlumniAdmin(admin.ModelAdmin):
    # Define the fields you want to display in the list view
    list_display = ('name', 'graduation_year', 'department', 'job_title', 'company', 'linkedin_profile')
    list_filter = ('graduation_year', 'department', 'job_title')  # Add filters
    search_fields = ( 'job_title', 'company')  # Add search fields
    ordering = ('-graduation_year',)  # Order by graduation year


admin.site.register(Alumni, AlumniAdmin)

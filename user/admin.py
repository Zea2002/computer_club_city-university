from django.contrib import admin
from .models import User

# Custom ModelAdmin for User
class UserAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'batch', 'is_admin', 'created_at')
    # Fields to filter by
    list_filter = ('is_admin', 'batch')
    # Fields to enable searching
    search_fields = ('username', 'email', 'batch')
    # Fields to display in the edit form
    fields = ('username', 'email', 'first_name', 'last_name', 'batch', 'is_admin', 'is_staff', 'is_superuser', 'groups', 'password', 'last_login', 'date_joined')
    # Read-only fields
    readonly_fields = ('last_login', 'date_joined', 'created_at')
    # Default ordering
    ordering = ('-created_at',)

# Register the User model with the custom ModelAdmin
admin.site.register(User, UserAdmin)

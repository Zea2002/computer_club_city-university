from django.contrib import admin
from .models import Executive

class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'linkedIn')  
    search_fields = ('user__username', 'designation')  
    list_filter = ('designation',)  
    ordering = ('user',)  

admin.site.register(Executive, ExecutiveAdmin)

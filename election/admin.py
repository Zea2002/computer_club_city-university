from django.contrib import admin
from .models import Candidate, Vote

# Candidate admin
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'votes')
    list_filter = ('position',)
    search_fields = ('user__first_name', 'user__last_name', 'position')

    # Allow sorting by votes
    ordering = ('-votes',)
    
    def save_model(self, request, obj, form, change):
        # Automatically update the number of votes when a candidate is saved
        super().save_model(request, obj, form, change)

# Vote admin
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate', 'position', 'created_at')
    list_filter = ('position', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'candidate__position')

    # Prevent direct modification of the votes in admin (to avoid tampering)
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Vote, VoteAdmin)

from django.contrib import admin
from .models import Candidate, Vote

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')
    search_fields = ('user__username', 'position')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'position')
    search_fields = ('voter__username', 'candidate__user__username', 'position')
    list_filter = ('position',)

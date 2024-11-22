from django.contrib import admin
from .models import Activity, Participant, Result

class ResultInline(admin.TabularInline):
    model = Result
    extra = 1  # How many empty result rows to display by default

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1  # How many empty participant rows to display by default

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'activity_type', 'date', 'time', 'location', 'online_link', 'created_at']
    list_filter = ['activity_type', 'date']
    search_fields = ['name', 'description']
    inlines = [ParticipantInline, ResultInline]  # Show participants and results directly in the activity admin

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'registered_at']
    list_filter = ['activity']
    search_fields = ['user__username', 'activity__name']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['activity', 'participant', 'rank', 'score', 'remarks']
    list_filter = ['activity']
    search_fields = ['activity__name', 'participant__user__username']
    ordering = ['activity', 'rank']

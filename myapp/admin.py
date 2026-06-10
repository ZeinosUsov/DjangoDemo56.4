from django.contrib import admin
from .models import Application, UserProfile

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'event_date', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'event_date')
    search_fields = ('title', 'user__username', 'user__profile__fio')
    list_editable = ('status',)
    fields = ('title', 'event_date', 'category', 'format', 'status', 'user', 'created_at', 'image')
    readonly_fields = ('created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fio', 'phone')
    search_fields = ('fio', 'phone', 'user__username')
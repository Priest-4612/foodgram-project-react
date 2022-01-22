from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email']
    list_display_links = ['pk', 'username']
    search_fields = ['username', 'email']
    list_filter = ['username', 'email']

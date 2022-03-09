from django.contrib import admin
from users.models import User, Subscribe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email']
    list_display_links = ['pk', 'username']
    search_fields = ['username', 'email']
    list_filter = ['username', 'email']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'subscriber', 'author']
    search_fields = ['subscriber', 'author']
    list_filter = ['subscriber', 'author']

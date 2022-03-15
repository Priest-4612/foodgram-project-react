from django.contrib import admin

from users.models import Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email']
    list_display_links = ['pk', 'username']
    search_fields = ['username', 'email']
    list_filter = ['username', 'email']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):

    list_display = ['pk', 'subscriber', 'author']
    search_fields = ['subscriber__email', 'author__email']
    list_filter = ['subscriber', 'author']

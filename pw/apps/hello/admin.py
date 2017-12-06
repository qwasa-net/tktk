from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = list_display


admin.site.register(User, UserAdmin)

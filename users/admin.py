from django.contrib import admin

from users.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ("id", "email", 'phone', 'country')
    ist_filter = ('email',)

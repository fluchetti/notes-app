from django.contrib import admin
from users.models import CustomUser
# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name', 'email')


admin.site.register(CustomUser, CustomUserAdmin)

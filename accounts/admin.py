from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = ('email','username','first_name','last_name', 'role' ,'is_active')
    ordering = ('-date_joined',)

admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)
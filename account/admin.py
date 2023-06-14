from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

admin.site.register(User)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'town_or_city', 'image_tag', 'postcode']
    readonly_fields = ['image_tag']

admin.site.register(Profile, ProfileAdmin)
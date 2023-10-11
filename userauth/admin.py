from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from registration.models import FamilyMember

class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['email', 'family_name', 'first_name', 'last_name', 'photo_consent', 'contact_number', 'pk']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('family_name', 'photo_consent', 'post_code', 'city', 'contact_number', 'additional_information',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('family_name', 'photo_consent', 'post_code', 'city', 'contact_number', 'additional_information',)}),
    )

    inlines = [
        FamilyMemberInline,
    ]

admin.site.register(CustomUser, CustomUserAdmin)
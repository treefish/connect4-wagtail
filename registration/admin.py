from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import FamilyMember, Parent, ParentMore, Child, ChildMore
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

class ParentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "id")
#    inlines = (ParentMoreInline, )
    readonly_fields = ("family", "type")
    search_fields = ["first_name", "last_name"]
    list_filter = ["last_name"]

    # fieldsets = (
    #     ('Personal', {
    #         'fields': (('first_name', 'last_name'), 'wp_member_id')
    #     }),
    #     ('Health & Wellbeing', {
    #         'fields': (('diet_req', 'diet_detail'), ('medical_req', 'medical_detail'))
    #     }),
    # )

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Parent, ParentAdmin)


class ChildMoreInline(admin.StackedInline):
    model = ChildMore

    fieldsets = (
        ('Personal', {
            'fields': (('dob', 'gender'), )
        }),
        ('Health & Wellbeing', {
            'fields': ('fsm', ('sen_req', 'sen_detail')),
        }),
        ('Education', {
            'fields': ('school',),
        }),
    )

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False


class ChildAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "family", "childmore", "id")
    inlines = (ChildMoreInline,)
    readonly_fields = ("family", "type")
    search_fields = ["first_name", "last_name", "family__family_name"]
    list_filter = ["last_name"]

    # fieldsets = (
    #     ('Personal', {
    #         'fields': (('first_name', 'last_name'), 'wp_member_id')
    #     }),
    #     ('Health & Wellbeing', {
    #         'fields': (('diet_req', 'diet_detail'), ('medical_req', 'medical_detail'))
    #     }),
    # )

    # fieldsets = (
    #     ('Health & Wellbeing', {
    #     # 'classes': ('collapse',),
    #         'fields': ('fsm', ('diet_req', 'diet_detail'), ('medical_req', 'medical_detail'), ('sen_req', 'sen_detail')),
    #     })
    # )

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Child, ChildAdmin)

# from django.contrib import admin
# from .models import Booking, Attendance
# from registration.models import FamilyMember
#
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ("event", "family", "booking_date")
#     search_fields = ["event", "family"]
#     list_filter = ["event", "family"]
#     autocomplete_fields = ["event", "family"]
#     save_on_top = True
#
# admin.site.register(Booking, BookingAdmin)
#
#
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ("family_member", "attended", "booking")
#     search_fields = ["booking", "family_member"]
#     list_filter = ["attended", "booking__event"]  # , "family_member"
#     autocomplete_fields = ["booking"]
#     save_on_top = True
#
# admin.site.register(Attendance, AttendanceAdmin)

from django.contrib import admin
from .models import Booking, Attendance
from events.models import EventPage
# from registration.models import FamilyMember

class EventPageAdmin(admin.ModelAdmin):
    list_display = ("description", "start_date", "end_date")
    search_fields = ["description", "start_date", "end_date"]
    list_filter = ["description", "start_date", "end_date"]

admin.site.register(EventPage, EventPageAdmin)


class AttendanceInline(admin.TabularInline):
    model = Attendance


class BookingAdmin(admin.ModelAdmin):
    list_display = ("event", "family", "booking_date")
    search_fields = ["event", "family"]
    list_filter = ["event", "family"]
    autocomplete_fields = ["event", "family"]
    save_on_top = True

    inlines = [
        AttendanceInline,
    ]

admin.site.register(Booking, BookingAdmin)

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

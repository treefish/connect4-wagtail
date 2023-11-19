from django.contrib import admin

from events.models import EventPage, EventType


class EventPageInline(admin.TabularInline):
    model = EventPage

    fields = ["title", "week", "start_date", "end_date", "capacity", "bookable"]


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

    inlines = (EventPageInline,)

admin.site.register(EventType, EventTypeAdmin)

#
# class AttendanceInline(admin.TabularInline):
#     model = Attendance

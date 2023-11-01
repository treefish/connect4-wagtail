from django.contrib import admin

from events.models import EventPage, EventType


class EventPageInline(admin.StackedInline):
    model = EventPage


# class EventTypeAdmin(admin.ModelAdmin):
#     list_display = ("name",)
#     # search_fields = ["name"]
#
#     inlines = (EventPageInline,)
#
# admin.site.register(EventType, EventTypeAdmin)

#
# class AttendanceInline(admin.TabularInline):
#     model = Attendance

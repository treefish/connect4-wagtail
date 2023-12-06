"""
Author..: David Apimerika
Created.: 24 May 2023
Updated.: 21 July 2023
          06 December 2023 (copied from connect4-django)

Purpose.:
"""

#import datetime
from datetime import date, time, datetime
import pytz
from dateutil.parser import parse
import itertools
from openpyxl import load_workbook, utils
from openpyxl.styles import Font, Fill, PatternFill
from copy import copy

# from django.db.models import Count
from django.contrib.auth import get_user_model

from events.models import EventPage
from bookings.models import Booking, Attendance

# from registration.models import Family, FamilyMember
# from registration.stats import FamilyMemberStats
# from events.models import Project, EventType, Event, Booking, Attendance

User = get_user_model()

########################################################################################################################
#                                                                                                                      #
########################################################################################################################
def create_attendance_register_daily(event, filename):
    workbook = load_workbook(filename="data/templates/attendance_register_daily.xlsx")
    workbook.iso_dates = True
    event_ws = workbook["Day Register"]
    ws_date_format = "%d-%b"
    tz = pytz.timezone('Pacific/Auckland')  # 'Europe/London'
    start_date = event.start_date
    ws_name = start_date.astimezone(tz).strftime(ws_date_format)
    run_dt = datetime.now().astimezone(tz).replace(tzinfo=None)
    event_date = start_date.astimezone(tz).replace(tzinfo=None)
    print(f"  - Event: {event}\t{ws_name}")
    event_ws.title = ws_name
    event_ws["B1"] = event.title
    event_ws["B2"] = event_date
    event_ws["B3"] = event.week
    event_ws["S1"] = event.id
#    event_ws["S2"] = event.wp_event_id
    event_ws["S4"] = run_dt

    # Loop through booked attendees and copy their info into a row for each, starting at Row 6.
    row = 7
    current_family_name = ""
    bookings = Booking.objects.filter(event=event)
    attendance_list = (
        Attendance.objects
#        .select_related("family_member__family")
        .select_related("booking__family")
        .filter(booking__in=bookings)
        .order_by(
            "booking__family__last_name",
            "booking__family__first_name",
        )
    )
    for attendee in attendance_list:
        row += 1
        family_member = attendee.family_member
        registrant = f"{attendee.booking.family.first_name} {attendee.booking.family.last_name}"
        print(f"    - Attendee: {row - 5}\t{family_member}")
        event_ws[f"A{row}"] = family_member.first_name
        event_ws[f"B{row}"] = family_member.last_name
        event_ws[f"E{row}"] = family_member.type.capitalize()
        event_ws[f"H{row}"] = 1 if attendee.attended else ""
        event_ws[f"R{row}"] = family_member.id
        if family_member.type == "CHILD":
            event_ws[f"C{row}"] = 1 if family_member.childmore.fsm else ""
            event_ws[f"D{row}"] = family_member.childmore.sen_detail
            event_ws[f"F{row}"] = family_member.childmore.dob

        family_name = family_member.family.family_name
        if not current_family_name == family_name:
            event_ws[f"S{row}"] = registrant
            event_ws[f"S{row}"].fill = copy(event_ws["S1"].fill)
            event_ws[f"T{row}"] = family_name
            event_ws[f"T{row}"].fill = copy(event_ws["S1"].fill)
            current_family_name = family_name

    # Save spreadsheet
    workbook.save(filename=f"media/admin/{filename}")
    workbook.close()
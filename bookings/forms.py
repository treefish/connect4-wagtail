from django import forms
from django.contrib.auth import get_user_model
from .models import Booking, Attendance
from events.models import EventPage

from django.utils import timezone

User = get_user_model()

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ('event',)

    def __init__(self, available_events=None, *args, **kwargs):
        '''
        available_events: A list of event ids to use in the drop-down select form for Event.
        Note: if available_events is an empty list, this means no event is bookable for the user, so presents a
        drop-down selection with no events.
        '''
        super(BookingForm, self).__init__(*args, **kwargs)
        if available_events is not None:
            self.fields['event'].queryset = EventPage.objects.filter(id__in=available_events)


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ('family_member', 'attended')



from django import forms
from django.contrib.auth import get_user_model
from .models import Booking, Attendance
from events.models import EventPage
from registration.models import FamilyMember

User = get_user_model()

class BookingForm(forms.ModelForm):

    attendees = forms.ModelMultipleChoiceField(
        queryset = None,
        widget = forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Booking
        fields = ('event',)

    def __init__(self, available_events=None, user=None, *args, **kwargs):
        print(f"* <<BookingForm>> init")
        '''
        available_events: A list of event ids to use in the drop-down select form for Event.
        Note: if available_events is an empty list, this means no event is bookable for the user, so presents a
        drop-down selection with no events.
        '''
        super(BookingForm, self).__init__(*args, **kwargs)
        if available_events is not None:
            self.fields['event'].queryset = EventPage.objects.filter(id__in=available_events)

        if user:
            self.fields['attendees'].queryset = FamilyMember.objects.filter(family=user)

    def clean(self):
        print(f"* <<BookingForm clean>>")
        super().clean()
        print(f"* <BookingForm>: Form Data: {self.data}")


class BookingUpdateForm(forms.ModelForm):
    # family_members = forms.ModelMultipleChoiceField(
    #     queryset = None,
    #     widget = forms.CheckboxSelectMultiple
    # )

    attendees = forms.ModelMultipleChoiceField(
        queryset = None,
        widget = forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Booking
        fields = ('booking_date',)
        widgets = {'booking_date': forms.HiddenInput()}

    def __init__(self, user=None, instance=None, *args, **kwargs):
        print(f"* <<BookingUpdateForm init>>")
        '''
        instance is a Booking
        '''
        super(BookingUpdateForm, self).__init__(*args, **kwargs)
        if instance:
            print(f"* <BookingUpdateForm>: Updating booked family members for booking: {instance}")
            # self.fields["event"] = instance.event
            self.fields["booking_date"].widget.attrs['readonly'] = True
            #self.fields['booking_date'].widget.attrs['hidden'] = True
            print(f"* - Event: {instance.event}")
            booked_attendees = Attendance.objects.filter(booking=instance)
#            self.fields['attendees'].queryset = booked_attendees
            print(f"* - Booked Attendees: {booked_attendees}")

            # This should be the Attendance objects, to pre-set the booked or not.
            self.fields['attendees'].queryset = FamilyMember.objects.filter(family=user)


        else:
            print(f"* <BookingUpdateForm>: Updating booked family members for booking: No booking!")

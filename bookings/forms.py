from django import forms
from django.core.exceptions import ValidationError
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
        '''
        All Events
        - Cannot exceed available spaces

        Family Fun Days
        - At least one Parent must attend, can be more.
        - At least one Child must attend.

        Youth Events
        - Only Children 11-16 (Secondary) can attend
        '''

        print(f"* <<BookingForm clean>>")
        cleaned_data = super().clean()
        event = cleaned_data.get("event")
        spaces_available = event.spaces_available
        attendees = cleaned_data.get("attendees")
        print(f"* <BookingForm>: Form Data: {self.data}")
        print(f"* <BookingForm>: Event: {event}")
        print(f"* <BookingForm>: Attendees: {attendees}")

        num_parents = 0
        num_children = 0
        num_ineligible_children = 0
        errors = {}
        for family_member in attendees:
            print(f"*  Checking {family_member.id} - {family_member} for eligibility")
            if family_member.type == FamilyMember.Types.CHILD:
                num_children += 1
                print(f"*    A Child - that makes {num_children}")
                if not family_member.childmore.is_secondary:
                    num_ineligible_children += 1
                    print(f"*    Child is {family_member.childmore.years_old} - that makes {num_ineligible_children}")
            else:
                num_parents += 1
                print(f"*    A Parent - that makes {num_parents}")

        if event.event_type.name == "Youth Events":
            if (num_parents > 0) or (num_ineligible_children > 0):
                errors["attendees"] = "Only Children 11-16 in Youth Events."
        elif event.event_type.name == "Family Fun Days":
            if (num_parents == 0) or (num_children == 0):
                errors["attendees"] = "Must have at least one Parent/Caregiver and at least one Child in Family Fun Days Events."
        if attendees.count() > spaces_available:
            errors["attendees"] = f"Too many attendees ({attendees.count()}) added for the number of spaces available for this event ({spaces_available})."

        if errors:
            raise ValidationError(errors)


class BookingUpdateForm(forms.ModelForm):

    attendees = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
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
            self.fields["booking_date"].widget.attrs['readonly'] = True
            self.event = instance.event
            self.booking = instance
            print(f"* - Event: {instance.event}")
            booked_attendees = Attendance.objects.filter(booking=instance)
            print(f"* - Booked Attendees: {booked_attendees}")

            # This should be the Attendance objects, to pre-set the booked or not.
            self.fields['attendees'].queryset = FamilyMember.objects.filter(family=user)
        else:
            print(f"* <BookingUpdateForm>: Updating booked family members for booking: No booking!")

    def clean(self):
        print(f"* <<BookingUpdateForm clean>>")
        '''
        All Events
        - Cannot exceed available spaces
        
        Family Fun Days
        - At least one Parent must attend, can be more.
        - At least one Child must attend.

        Youth Events
        - Only Children 11-16 (Secondary) can attend
        '''
        print(f"* <<BookingUpdateForm clean>>")
        cleaned_data = super().clean()

        event = self.event # From __init__() above
        spaces_available = event.spaces_available
        currently_booked_spaces = self.booking.attendance_set.all().count()
        attendees = cleaned_data.get("attendees")
        print(f"* <BookingUpdateForm>: Form Data: {self.data}")
        print(f"* <BookingUpdateForm>: Booking: {self.booking}")
        print(f"* <BookingUpdateForm>: Event: {event}")
        print(f"* <BookingUpdateForm>: Attendees: ({currently_booked_spaces}) - {attendees}")

        num_parents = 0
        num_children = 0
        num_ineligible_children = 0
        errors = {}
        for family_member in attendees:
            print(f"*  Checking {family_member.id} - {family_member} for eligibility")
            if family_member.type == FamilyMember.Types.CHILD:
                num_children += 1
                print(f"*    A Child - that makes {num_children}")
                if not family_member.childmore.is_secondary:
                    num_ineligible_children += 1
                    print(f"*    Child is {family_member.childmore.years_old} - that makes {num_ineligible_children}")
            else:
                num_parents += 1
                print(f"*    A Parent - that makes {num_parents}")

        if event.event_type.name == "Youth Events":
            if (num_parents > 0) or (num_ineligible_children > 0):
                errors["attendees"] = "Only Children 11-16 in Youth Events."
        elif event.event_type.name == "Family Fun Days":
            if (num_parents == 0) or (num_children == 0):
                errors["attendees"] = "Must have at least one Parent/Caregiver and at least one Child in Family Fun Days Events."
        if attendees.count() > spaces_available + currently_booked_spaces:
            errors["attendees"] = f"Too many attendees ({attendees.count()}) added for the number of spaces available for this event ({spaces_available})."

        if errors:
            raise ValidationError(errors)
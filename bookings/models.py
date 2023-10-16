from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from registration.models import FamilyMember

# from dateutil.relativedelta import relativedelta
# from datetime import *

User = get_user_model()


class Booking(models.Model):
    family = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventPage, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(help_text='Booking date/time', default=timezone.now)
#    status = models.BooleanField("Booked or Cancelled?", default=False)
#    cancelled_date = models.DateTimeField(help_text='Booking cancelled date/time', default=timezone.now)

    class Meta:
        ordering = ["-booking_date"]
        unique_together = ('family', 'event',)

    def __str__(self):
        return f"{self.family} - {self.event} - {self.booking_date}"


class Attendance(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    # Note Attendee must be a FamilyMember of the Family that Booked.
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    attended = models.BooleanField("Attended event?", default=False)

    def __str__(self):
        return f"{self.family_member} - {self.attended}"

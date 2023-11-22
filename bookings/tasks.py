from django.utils.timezone import localdate, localtime

from celery import shared_task
from django.core.mail import EmailMessage
from bookings.models import Booking

@shared_task
def adding_task(x, y):
    ans = x + y
    print(f"* Celery task: Adding - {x} + {y} = {ans}")
    return ans


@shared_task()
def send_booking_email_task(booking_id):
    print("* Sending e-mail message using send_booking_email_task()")
    booking = Booking.objects.get(id=booking_id)
    event = booking.event
    user = booking.family
    attendees = booking.attendance_set.all()
    names = set(f"{attendee.family_member.first_name} {attendee.family_member.last_name}" for attendee in attendees)
    attendee_names = ", ".join(names)

    recipients = [user.email]
    bcc = ["connect4@treefish.co.nz"]
    subject = f"Connect4Families Event Booking - {event.title}"
    body = f'''
Hello {user.first_name},

Thank you for your booking, please save the date in your calendar. The full details of your booking are shown below:

  Event: {event.title}
  Date.: {localdate(event.start_date).strftime("%d/%m/%Y")}
  Time.: {localtime(event.start_date).strftime("%H:%M %p")} - {localtime(event.end_date).strftime("%H:%M %p")}

The following people in your group are booked to come to this event:

  {attendee_names}

Please arrive in time to complete checking-in and prepare for the event. If you cannot make it to the event, please cancel as soon as possible on-line to allow other families to book and attend.

Note: We reserve the right to cancel or introduce new guidelines resulting from Government notifications.

We look forward to welcoming you.

Best wishes
Connect4Families Team
'''

    email = EmailMessage(subject, body, "connect4@treefish.co.nz", recipients, bcc)
    #    reply_to=["another@example.com"],
    #    headers={"Message-ID": "foo"},
    email.send()


@shared_task()
def send_booking_cancellation_email_task(booking_id):
    print("* Sending e-mail message using send_booking_cancellation_email_task()")
    booking = Booking.objects.get(id=booking_id)
    event = booking.event
    user = booking.family
    attendees = booking.attendance_set.all()
    names = set(f"{attendee.family_member.first_name} {attendee.family_member.last_name}" for attendee in attendees)
    attendee_names = ", ".join(names)

    recipients = [user.email]
    bcc = ["connect4@treefish.co.nz"]
    subject = f"Connect4Families Event Booking Cancellation - {event.title}"
    body = f'''
Hello {user.first_name},

Thank you for your cancellation of this booking, this action enables other families to book this event. The full details of the booking you are cancelling are shown below:

  Event: {event.title}
  Date.: {localdate(event.start_date).strftime("%d/%m/%Y")}
  Time.: {localdate(vent.start_date).strftime("%H:%M %p")} - {localdate(event.end_date).strftime("%H:%M %p")}

The following people in your group were booked to come to this event:

  {attendee_names}

We look forward to welcoming you to a future event.

Best wishes
Connect4Families Team
'''

    email = EmailMessage(subject, body, "connect4@treefish.co.nz", recipients, bcc)
    #    reply_to=["another@example.com"],
    #    headers={"Message-ID": "foo"},
    email.send()

    # Delete the booking here because we have to wait for the e-mail to be sent.
    booking.delete()
from celery import shared_task
from django.core.mail import EmailMessage
from bookings.models import Booking

# @shared_task
# def adding_task(x, y):
#     ans = x + y
#     print(f"* Celery task: Adding - {x} + {y} = {ans}")
#     return ans


@shared_task()
def send_booking_email_task(id):
    print("* Sending e-mail message using Celery!")
    booking = Booking.objects.get(id=id)
    event = booking.event
    user = booking.family
    attendees = booking.attendance_set.all()
    names = set(f"{attendee.family_member.first_name} {attendee.family_member.last_name}" for attendee in attendees)
    attendee_names = ", ".join(names)

    recipients = [user.email]
    bcc = ["wagtail@treefish.co.nz"]
    subject = "Connect4Families Event Booking"
    body = f'''
Hello {user.first_name},

You have successfully booked for the following Connect4Families event: 

  Event: {event}
  Date.: {event.start_date.strftime("%d/%m/%Y")}
  Time.: {event.start_date.strftime("%H:%M %p")} - {event.end_date.strftime("%H:%M %p")}

The following people are booked to come to this event:

  {attendee_names}

Please arrive in time to complete checking-in and prepare for the event. If you cannot make it to the event, please cancel as soon as possible on-line to allow other families to book and attend.

We look forward to seeing you.

Regards
Connect4Familes team
'''

    email = EmailMessage(subject, body, "wagtail@treefish.co.nz", recipients, bcc)
    #    reply_to=["another@example.com"],
    #    headers={"Message-ID": "foo"},
    email.send()

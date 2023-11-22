from django.utils import timezone

from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
# from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

from .tasks import send_booking_email_task, send_booking_cancellation_email_task  # adding_task
from django.contrib.auth import get_user_model
from .models import Booking, Attendance
from .forms import BookingForm, BookingUpdateForm
from events.models import EventPage
from registration.models import FamilyMember

User = get_user_model()

class BookingsBaseView(View):
    model = Booking
    fields = '__all__'
#    success_url = reverse_lazy('events:events')


class BookingsListView(BookingsBaseView, ListView):
    """View to list all bookings for a Family (User).
     Use the 'booking_list' variable in the template
     to access all Booking objects"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        booking_list = Booking.objects.filter(family=user).order_by("event__start_date")
        context['booking_list'] = booking_list
        return context


def available_events(user):
    '''
    This will return a list of event ids that the family (logged in user) can book. Criteria are:
    - Events that are Published (Live)
    - Events with a start_date in the future (cannot book an event that has started or is in the past)
    - Events that are set to bookable (a field of EventPage)
    - Events that the family have not already booked (check current bookings and exclude events)

    Note: It would be better to do this more cleanly in the form (by passing in the queryset), but this works for now.
    '''
    family_bookings = Booking.objects.filter(family=user)
    ids = [booking.event.id for booking in family_bookings]
    # available_events = EventPage.objects.live().filter(start_date__gt=timezone.now()).filter(bookable=True).exclude(id__in=ids)
    available_events = EventPage.objects.live().filter(start_date__gt=timezone.now()).exclude(id__in=ids)
    ids = [
        event.id
        for event in available_events
    ]

    # Slow way to restrict events to those with capacity
    available_event_ids = []
    for event in EventPage.objects.filter(id__in=ids):
        if event.spaces_available > 0:
            available_event_ids.append(event.id)
        else:
            print("No spaces left!")

    return available_event_ids  # ids #available_events


@login_required
def create_booking(request):
    print(f"* <<create_booking>>")
    user = User.objects.get(id=request.user.id)
    booking_list = Booking.objects.filter(family=user).order_by("event__start_date")
    ids = available_events(user)
    form = BookingForm(data=request.POST or None, available_events=ids, user=user)

    if request.method == "POST":
        if form.is_valid():
            booking = form.save(commit=False)
            booking.family = user
            booking.save()
            #ans = adding_task.delay(3, 7) -- just testing Celery
            # Cannot send an object to a task - https://stackoverflow.com/questions/49373825/kombu-exceptions-encodeerror-user-is-not-json-serializable
            send_booking_email_task.delay(booking.id)

            # Handle list of ticked booked family members.
            booked_attendees = request.POST.getlist('attendees')
            for id in booked_attendees:
                family_member = FamilyMember.objects.get(id=id)
                print(f"* <create_booking>: Booked to come: {family_member}")
                attendance, created = Attendance.objects.get_or_create(booking=booking, family_member=family_member)
                if created:
                    print(f"* <create_booking>: Creating booked atendance for {family_member}")
                else:
                    print(f"* <create_booking>: Updating booked attendance for {family_member}")

            return redirect("detail-booking", pk=booking.id)
        else:
            return render(request, "bookings/partials/booking_form.html", context={
                "form": form,
            })

    context = {
        "form": form,
        "user": user,
        "booking_list": booking_list
    }

    return render(request, "bookings/booking_list.html", context)


@login_required
def create_booking_form(request):
    print(f"* <<create_booking_form>>")
    user = User.objects.get(id=request.user.id)
    ids = available_events(user)
    form = BookingForm(data=None, available_events=ids, user=user)
    context = {
        "form": form
    }
    return render(request, "bookings/partials/booking_form.html", context)


@login_required
def detail_booking(request, pk):
    print(f"* <<detail_booking>>")
    booking = get_object_or_404(Booking, id=pk)
    booked_attendees = Attendance.objects.filter(booking=booking)
    print(f"* <detail_booking>: Attendees: {booked_attendees}")
    context = {
        "booking": booking,
        "booked_attendees": booked_attendees,
    }
    return render(request, "bookings/partials/booking_detail.html", context)


@login_required
def update_booking_attendees(request, pk):
    print(f"* <<update_booking_attendees>>")
    user = User.objects.get(id=request.user.id)
    booking = Booking.objects.get(id=pk)
    booked_attendees = Attendance.objects.filter(booking=booking)

    form = BookingUpdateForm(data=request.POST or None, user=user, instance=booking) #, initial={"attendees": booked_attendees})
    print(f"* <update_booking_attendees>: Updating Booking for {user} for booking {booking}")
    if request.method == "POST":
        if form.is_valid():
            # Update booking date
            #booking = form.save(commit=False)
            booking.booking_date = timezone.now()
            booking.save()
            send_booking_email_task.delay(booking.id)
            # Remove current bookings
            booked_attendees.delete()
            # handle list of ticked booked family members.
            booked_attendees = request.POST.getlist('attendees')
            for id in booked_attendees:
                family_member = FamilyMember.objects.get(id=id)
                print(f"* <update_booking_attendees>: Booked to come: {family_member}")
                attendance, created = Attendance.objects.get_or_create(booking=booking, family_member=family_member)
                if created:
                    print(f"* <update_booking_attendees>: Creating booked attendance for {family_member}")
                else:
                    print(f"* <update_booking_attendees>: Updating booked attendance for {family_member}")

            return redirect("detail-booking", pk=booking.id)
        else:
            return render(request, "bookings/partials/booking_form.html", context={
                "form": form,
                "booking": booking
            })
    else:
        print(f"* <update_booking_attendees>: Need to pre-populate form & booking (Attendance)")

    context = {
        "form": form,
        "booking": booking
    }

    return render(request, "bookings/partials/booking_form.html", context)


@login_required
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, id=pk)

    if request.method == "POST":
        booking.delete()
        send_booking_cancellation_email_task.delay(booking.id)
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )

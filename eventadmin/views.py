#from django.views.generic import TemplateView
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from events.models import ProjectPage, EventPage
from bookings.models import Booking, Attendance
from django.db.models import Count

# For Function based views
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

#from .forms import forms
# For Wordpress stuff
#from .utils import *
from .utils import (
    create_attendance_register_daily,
)

def is_member(user):
    # Used to restrict access to sensitive pages.
    return user.is_superuser or user.groups.filter(name='Editors').exists()


### Events
class EventBaseView(View):
    model = EventPage
    fields = '__all__'
    success_url = reverse_lazy('eventadmin:events')


class EventListView(LoginRequiredMixin, UserPassesTestMixin, EventBaseView, ListView):
    """View to list all events.
     Use the 'eventpage_list' variable in the template
     to access all Event objects"""

    template_name = 'eventadmin/event_list.html'

    def test_func(self):
        return is_member(self.request.user)


class EventDetailView(LoginRequiredMixin, UserPassesTestMixin, EventBaseView, DetailView):
    """View to list the details from one event.
    Use the 'event' variable in the template to access
    the specific event here and in the Views below"""

    template_name = 'eventadmin/event_detail.html'

    def test_func(self):
        return is_member(self.request.user)


class EventBookingsListView(LoginRequiredMixin, UserPassesTestMixin, EventBaseView, DetailView):
    """View to list the details from one event.
    Use the 'event' variable in the template to access
    the specific event here and in the Views below"""

    template_name = 'eventadmin/event_bookings_list.html'

    def test_func(self):
        return is_member(self.request.user)


########################################################################################################################
# Reporting
# These functions/classes are taken from connect4-django app
########################################################################################################################

class EventAttendanceView(EventBaseView, DetailView):
    template_name = 'eventadmin/event_attendance_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs['pk']
        print(f"Event ID: {event_id}")
        stats = {}

        attendance_list = Attendance.objects.select_related('family_member').filter(booking__event=event_id).select_related('family_member__childmore')
        stats['registered_total'] = attendance_list.count()

        parents_list = attendance_list.filter(family_member__type='PARENT')
        stats['parents_attended_total'] = parents_list.filter(attended=True).count()
        stats['parents_not_attended_total'] = parents_list.filter(attended=False).count()
        stats['parents_total'] = stats['parents_attended_total'] + stats['parents_not_attended_total']

        children_list = attendance_list.filter(family_member__type='CHILD')
        children_attended_list = children_list.filter(attended=True)
        children_not_attended_list = children_list.filter(attended=False)

        # Child (< 4>) Toddler / Youngster
        ids = [attendance.id for attendance in children_attended_list if attendance.family_member.childmore.is_youngster]
        stats['children_lt_4_attended_total'] = children_attended_list.filter(id__in=ids).count()
        ids = [attendance.id for attendance in children_not_attended_list if attendance.family_member.childmore.is_youngster]
        stats['children_lt_4_not_attended_total'] = children_not_attended_list.filter(id__in=ids).count()
        stats['children_lt_4_total'] = stats['children_lt_4_attended_total'] + stats['children_lt_4_not_attended_total']

        # Child (4-10) Primary
        ids = [attendance.id for attendance in children_attended_list if attendance.family_member.childmore.is_child]
        stats['children_4_10_attended_total'] = children_attended_list.filter(id__in=ids).count()
        ids = [attendance.id for attendance in children_not_attended_list if attendance.family_member.childmore.is_child]
        stats['children_4_10_not_attended_total'] = children_not_attended_list.filter(id__in=ids).count()
        stats['children_4_10_total'] = stats['children_4_10_attended_total'] + stats['children_4_10_not_attended_total']

        # Child (11-16) Secondary / Teenager
        ids = [attendance.id for attendance in children_attended_list if attendance.family_member.childmore.is_teenager]
        stats['teens_attended_total'] = children_attended_list.filter(id__in=ids).count()
        ids = [attendance.id for attendance in children_not_attended_list if attendance.family_member.childmore.is_teenager]
        stats['teens_not_attended_total'] = children_not_attended_list.filter(id__in=ids).count()
        stats['teens_total'] = stats['teens_attended_total'] + stats['teens_not_attended_total']

        # Child (> 16) Post-teen
        ids = [attendance.id for attendance in children_attended_list if attendance.family_member.childmore.is_post_teen]
        stats['post_teens_attended_total'] = children_attended_list.filter(id__in=ids).count()
        ids = [attendance.id for attendance in children_not_attended_list if attendance.family_member.childmore.is_post_teen]
        stats['post_teens_not_attended_total'] = children_not_attended_list.filter(id__in=ids).count()
        stats['post_teens_total'] = stats['post_teens_attended_total'] + stats['post_teens_not_attended_total']

        stats['attended_total'] = stats['parents_attended_total'] \
                                + stats['children_lt_4_attended_total'] \
                                + stats['children_4_10_attended_total'] \
                                + stats['teens_attended_total'] \
                                + stats['post_teens_attended_total']

        stats['not_attended_total'] = stats['parents_not_attended_total'] \
                                + stats['children_lt_4_not_attended_total'] \
                                + stats['children_4_10_not_attended_total'] \
                                + stats['teens_not_attended_total'] \
                                + stats['post_teens_not_attended_total']

        # Children 4-10 Attended, FSM, SEN
        ids = [attendance.id for attendance in children_attended_list if (attendance.family_member.childmore.is_child and attendance.family_member.childmore.fsm and attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tChildren 4-10 Attended, FSM, SEN")
        stats['children_4_10_attended_fsm_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Children 4-10 Attended, FSM, Non-SEN
        ids = [attendance.id for attendance in children_attended_list if (attendance.family_member.childmore.is_child and attendance.family_member.childmore.fsm and not attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tChildren 4-10 Attended, FSM, non-SEN")
        stats['children_4_10_attended_fsm_non_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Children 4-10 Attended, non-FSM, SEN
        ids = [attendance.id for attendance in children_attended_list if (
                    attendance.family_member.childmore.is_child and not attendance.family_member.childmore.fsm and attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tChildren 4-10 Attended, non-FSM, SEN")
        stats['children_4_10_attended_non_fsm_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Children 4-10 Attended, non-FSM, Non-SEN
        ids = [attendance.id for attendance in children_attended_list if (
                    attendance.family_member.childmore.is_child and not attendance.family_member.childmore.fsm and not attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tChildren 4-10 Attended, non-FSM, non-SEN")
        stats['children_4_10_attended_non_fsm_non_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Teenager Attended, FSM, SEN
        ids = [attendance.id for attendance in children_attended_list if (attendance.family_member.childmore.is_teenager and attendance.family_member.childmore.fsm and attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tTeenager Attended, FSM, SEN")
        stats['teens_attended_fsm_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Teenager Attended, FSM, Non-SEN
        ids = [attendance.id for attendance in children_attended_list if (attendance.family_member.childmore.is_teenager and attendance.family_member.childmore.fsm and not attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tTeenager Attended, FSM, non-SEN")
        stats['teens_attended_fsm_non_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Teenager Attended, non-FSM, SEN
        ids = [attendance.id for attendance in children_attended_list if (
                    attendance.family_member.childmore.is_teenager and not attendance.family_member.childmore.fsm and attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tTeenager Attended, non-FSM, SEN")
        stats['teens_attended_non_fsm_sen_total'] = children_attended_list.filter(id__in=ids).count()

        # Teenager Attended, non-FSM, Non-SEN
        ids = [attendance.id for attendance in children_attended_list if (
                    attendance.family_member.childmore.is_teenager and not attendance.family_member.childmore.fsm and not attendance.family_member.childmore.sen_req)]
        print(f"ids: {len(ids)}\tTeenager Attended, non-FSM, non-SEN")
        stats['teens_attended_non_fsm_non_sen_total'] = children_attended_list.filter(id__in=ids).count()

        context['stats'] = stats
        context['attendance_list'] = attendance_list
        print(f"Stats: {stats}")
        return context


class DownloadAttendanceRegisterDaily(EventBaseView, DetailView):
    template_name = 'eventadmin/download_attendance_register.html'

    def get(self, request, *args, **kwargs):
        event = super().get_object()
        filename = f"Attendance Register Daily - {event.title}.xlsx"
        create_attendance_register_daily(event, filename)
        success_url = f"/media/admin/{filename}"
        return redirect(success_url)
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
# from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect

#from .forms import forms
# For Wordpress stuff
#from .utils import *


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
     Use the 'event_list' variable in the template
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
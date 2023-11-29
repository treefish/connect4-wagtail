import re

# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# For aggregation
# from django.db.models import Count
from django.db.models import Q

from django.contrib.auth import get_user_model
# from bookings.models import Booking, Attendance
# from events.models import EventPage
# from registration.models import FamilyMember

regex = re.compile('[^\da-zA-Z]')
User = get_user_model()


def is_member(user):
    # Used to restrict access to sensitive pages.
    return user.is_superuser or user.groups.filter(name='Editors').exists()


class FamilyBaseView(View):
    model = User
    fields = '__all__'


class FamilyListView(LoginRequiredMixin, UserPassesTestMixin, FamilyBaseView, ListView):
    template_name = 'familyadmin/family_list.html'
    context_object_name = 'family_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure q is a string in case a number is searched - e.g. student username starts with intake year.
        q = self.request.GET.get("q", "")

        if q:
            # First parameter is the replacement, second parameter is your input string
            qname = regex.sub('', q)

            context['qname'] = qname
        return context

    def get_queryset(self):
        q = self.request.GET.get("q")
        if q:
            return User.objects.filter(
                Q(family_name__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
            )


    def test_func(self):
        return is_member(self.request.user)


class FamilyDetailView(LoginRequiredMixin, UserPassesTestMixin, FamilyBaseView, DetailView):
    template_name = 'familyadmin/family_detail.html'
    context_object_name = 'family'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Should be able to drill down through user (family), but here it is for now...
        # family_members = FamilyMember.objects.filter(family=self)
        # context['family_members'] = family_members
        return context


    def test_func(self):
        return is_member(self.request.user)

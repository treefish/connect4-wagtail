from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CustomUserUpdateForm
from registration.models import FamilyMember

User = get_user_model()

'''
Need to think about allowing users to delete their account:
- They have the right, but...
- We need the data for reporting.

If a user deleted their profile after an event (that they and family members attended), then we'd lose that data.
'''

class CustomUserUpdateView(UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('account_profile')

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)


class CustomUserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('account_signup')


class ProfileView(LoginRequiredMixin, DetailView):
    """Generic class-based view Family, Family members on current user."""
    model = User

    context_object_name = "family"
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.get(id=request.user.id)
        family_members = FamilyMember.objects.filter(family=user)
        context['user'] = user
        context['family_members'] = family_members
#        context['bookings'] = Booking.objects.filter(family__registrant=self.request.user)
        #print(f"Family: {context['family']}")
        return context

# def profile_view(request):
#     return render(request, 'account/profile.html')

def profile_view(request):
    user = User.objects.get(id=request.user.id)
    family_members = FamilyMember.objects.filter(family=user)
    context = {"user": user, "family_members": family_members}

    return render(request, 'account/profile.html', context)


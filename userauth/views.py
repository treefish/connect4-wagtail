from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserUpdateForm
from registration.models import FamilyMember

'''
Need to think about allowing users to delete their account:
- They have the right, but...
- We need the data for reporting.

If a user deleted their profile after an event (that they and family members attended), then we'd lose that data.
'''

class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)


class CustomUserDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('account_signup')


# def profile_view(request):
#     return render(request, 'account/profile.html')

def profile_view(request):
    user = CustomUser.objects.get(id=request.user.id)
    family_members = FamilyMember.objects.filter(family=user)
    context = {"user": user, "family_members": family_members}

    return render(request, 'account/profile.html', context)


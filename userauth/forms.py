from .models import CustomUser
from wagtail.users.forms import UserCreationForm, UserEditForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

class WagtailUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
#        widgets = {'dob': forms.DateInput(attrs={'type':'date'})}


class WagtailUserEditForm(UserEditForm):
    class Meta(UserEditForm.Meta):
        model = CustomUser
#        widgets = {'dob': forms.DateInput(attrs={'type':'date'})}


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_("First name"))
    last_name = forms.CharField(max_length=30, label=_("Last name"))
    family_name = forms.CharField(max_length=30, label=_("Family name"), help_text=_("e.g. The Addams Family"))
    photo_consent = forms.CharField(max_length=30, label=_("Photo consent?"), help_text=_("Allow photography of family for promotional use?"))
    post_code = forms.CharField(max_length=30, label=_("Post Code"), help_text=_("e.g. PO3 5HL"))
    city = forms.CharField(max_length=30, label=_("City"), help_text=_("e.g. Havant"))
    contact_number = forms.CharField(max_length=30, label=_("Contact Number"), help_text=_("e.g. +615555555"))
    additional_information = forms.CharField(max_length=30, label=_("Additional information"), help_text=_("Information of importance for event staff to know about your family."))


    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.family_name = self.cleaned_data['family_name']
        user.photo_consent = self.cleaned_data['photo_consent']
        user.post_code = self.cleaned_data['post_code']
        user.city = self.cleaned_data['city']
        user.contact_number = self.cleaned_data['contact_number']
        user.additional_information = self.cleaned_data['additional_information']
        user.save()


class CustomUserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'family_name', 'photo_consent', 'post_code', 'city', 'contact_number', 'additional_information',]
# TODO: Get a widget for True/False for Photo Consent
        CHOICES = [(True, "Yes"), (False, "No")]
#        widgets = {'photo_consent': forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)}

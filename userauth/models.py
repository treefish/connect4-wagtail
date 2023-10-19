from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CustomUser(AbstractUser):
    family_name = models.CharField("Family Name", max_length=70, default='Please provide a name for the family.', help_text='e.g. The Addams Family')
    # For the Family Members
    photo_consent = models.BooleanField("Photo consent?", default=False, help_text='Allow photos to be taken of anyone in the family? These may be used, for e.g., in Connect4 publicity or PCS newsletters.')
    post_code = models.CharField(verbose_name=_("Post Code"), max_length=12, blank=True, null=True, help_text='e.g. PO9 4BU')
    city = models.CharField(verbose_name=_("Town/City"), max_length=50, blank=True, null=True, help_text='e.g. Havant')
    phone_regex = RegexValidator(regex=r"^\+(?:[0-9]●?){6,14}[0-9]$", message=_("Enter a valid international mobile phone number starting with +(country code)"))
    contact_number = models.CharField(validators=[phone_regex], verbose_name=_("Contact mobile phone"), max_length=17, blank=True, null=True, help_text='e.g. +612392489800')
    additional_information = models.CharField(verbose_name=_("Additional information"), max_length=4096, blank=True, null=True, help_text='e.g. Family is sensitive to bright light.')

    class Meta:
        ordering = ['last_name']


    def get_absolute_url(self):
        return reverse('account_profile')


    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


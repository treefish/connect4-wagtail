from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField


@register_setting
class HoursSettings(BaseGenericSetting):

    hours = RichTextField(
        blank=True,
        null=True,
        features=[]
    )

    panels = [
        FieldPanel("hours"),
    ]


@register_setting
class ContactSettings(BaseGenericSetting):

    contact = RichTextField(
        blank=True,
        null=True,
        features=["link"]
    )

    panels = [
        FieldPanel("contact"),
    ]


@register_setting
class SocialMediaSettings(BaseGenericSetting):

    facebook = models.URLField(
        blank=True,
        help_text="Enter your Facebook URL"
    )
    twitter = models.URLField(
        blank=True,
        help_text="Enter your Twitter URL"
    )
    instagram = models.URLField(
        blank=True,
        help_text="Enter your Instagram URL"
    )
    youtube = models.URLField(
        blank=True,
        help_text="Enter your YouTube URL"
    )

    panels = [
        FieldPanel("facebook"),
        FieldPanel("twitter"),
        FieldPanel("instagram"),
        FieldPanel("youtube"),
    ]
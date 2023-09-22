from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
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

    def save(self, *args, **kwargs):
         key = make_template_fragment_key("footer_hours_settings")
         cache.delete(key)

         return super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
         key = make_template_fragment_key("footer_contact_settings")
         cache.delete(key)

         return super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
         key = make_template_fragment_key("footer_social_settings")
         cache.delete(key)

         return super().save(*args, **kwargs)
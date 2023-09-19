from django.db import models
#from django.core.exceptions import ValidationError

from wagtail.models import Page
#from wagtail.admin.panels import FieldPanel


class FlexPage(Page):
#    template = "services/service_listing_page.html"

    class Meta:
        verbose_name = "Flex (misc) page"
        verbose_name_plural = "Flex (misc) pages"
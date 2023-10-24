from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class PartnerListingPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["partners.PartnerPage"]
    max_count = 1

    template = "partners/partner_listing_page.html"
    subtitle = models.TextField(blank=True, max_length=500)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["partners"] = PartnerPage.objects.live().public()
        return context


class PartnerPage(Page):
    parent_page_types = ["partners.PartnerListingPage"]
    subpage_types = []
    template = "partners/partner_page.html"

    name = models.TextField(blank=False, null=False, max_length=100)
    internal_page = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        related_name="+",
        help_text="Select an internal Wagtail page",
        on_delete=models.SET_NULL,
    )
    external_page = models.URLField(blank=True)
    button_text = models.CharField(blank=True, max_length=50)
    partner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text="This image will be used on the Partner Listing Page and will be cropped to 570px by 370px on this page.",
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("internal_page"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        FieldPanel("partner_image"),
    ]

    def clean(self):
        super().clean()

        if self.internal_page and self.external_page:
            # Both fields are filled out
            raise ValidationError({
                "internal_page": ValidationError("Please only select a page OR an external URL"),
                "external_page": ValidationError("Please only select a page OR an external URL")
            })

        if not self.internal_page and not self.external_page:
            # Both fields are filled out
            raise ValidationError({
                "internal_page": ValidationError("Please select either a page OR an external URL"),
                "external_page": ValidationError("Please select either a page OR an external URL")
            })

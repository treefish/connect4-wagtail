from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


########################################################################################################################
#
# Projects
#
########################################################################################################################
class ProjectListingPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["events.ProjectPage"]
    max_count = 1

    template = "events/project_listing_page.html"
    subtitle = models.TextField(blank=True, max_length=500)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["projects"] = ProjectPage.objects.live().public()
        return context


class ProjectPage(Page):
    parent_page_types = ["events.ProjectListingPage"]
    subpage_types = ["events.EventPage"]
    template = "events/project_page.html"

    description = models.TextField(blank=True, max_length=500)
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
    project_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text="This image will be used on the Project Listing Page and will be cropped to 570px by 370px on this page.",
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("internal_page"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        FieldPanel("project_image"),
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


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["events"] = EventPage.objects.live().public()
        return context


########################################################################################################################
#
# Events
#
########################################################################################################################
# class EventListingPage(Page):
#     parent_page_types = ["events.ProjectPage"]
#     subpage_types = ["events.EventPage"]
#     max_count = 1
#
#     template = "events/event_listing_page.html"
#     subtitle = models.TextField(blank=True, max_length=500)
#
#     content_panels = Page.content_panels + [
#         FieldPanel("subtitle"),
#     ]
#
#     def get_context(self, request, *args, **kwargs):
#         context = super().get_context(request, *args, **kwargs)
#         context["events"] = EventPage.objects.live().public()  # Need to limit to Events in this Project
#         return context


class EventPage(Page):
    parent_page_types = ["events.ProjectPage"]
    subpage_types = []
    template = "events/event_page.html"

    description = models.TextField(blank=True, max_length=500)
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
    event_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text="This image will be used on the Project Page and will be cropped to 570px by 370px on this page.",
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("internal_page"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        FieldPanel("event_image"),
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


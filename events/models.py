from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, FieldRowPanel



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


class EventType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


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

    # From Connect4-Django
    # Note: default=timezone.now() for dates
    start_date = models.DateTimeField("Start Date", help_text='Event start date/time')
    end_date = models.DateTimeField("End Date", blank=True, null=True, help_text='Event end date/time')
    event_type = models.CharField(blank=True, max_length=50)

#    event_type = models.ForeignKey(EventType, null=True, on_delete=models.SET_NULL, related_name="event_type") #, default = 1
#    event_website = models.URLField(blank=True, null=True, help_text='Optional external link for the event or programme')
#    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="venue", default = 1)
    capacity = models.PositiveSmallIntegerField("Capacity", default=300)  # Default to Venue capacity somehow. Override Save?
#    visible = models.BooleanField("Event visible?", default=False) # Use Draft or Publish state
    bookable = models.BooleanField("Event bookable?", default=False, help_text='Allow bookings for this event?')
#    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project")
    week = models.PositiveSmallIntegerField("Event week", default=1)
#    wp_event_id = models.PositiveIntegerField("Wordpress Event ID", blank=True, null=True)


    content_panels = Page.content_panels + [
        FieldPanel("description"),

        FieldPanel("internal_page"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        FieldPanel("event_image"),
        FieldRowPanel(
            [
                FieldPanel("week"),
                FieldPanel("start_date"),
                FieldPanel("end_date")
            ]
        ),
        # FieldPanel("event_type"),
        FieldPanel("capacity"),
        FieldPanel("bookable"),

    ]

    @property
    def event_passed(self):
        return self.end_date < timezone.now()

    @property
    def event_now(self):
        return self.start_date < timezone.now() < self.end_date

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

        # end_date must not be before start_date (can be the same day).
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({"end_date": "The end date must be the same or after the start date."})


    class Meta:
        ordering = ["-start_date"]
from django.db import models

from django_extensions.db.fields import AutoSlugField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, PageChooserPanel, InlinePanel


class MenuItem(Orderable):
    link_title = models.CharField(max_length=50,blank=True)
    link_url = models.CharField(max_length=500,blank=True)
    link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    page = ParentalKey("Menu", related_name="menu_items")


class Menu(ClusterableModel):

    title = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from="title",
        editable=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Item"),
    ]

    def __str__(self):
        return self.title
from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from streams import blocks


""" From docs - https://docs.wagtail.org/en/v5.1.1/reference/contrib/table_block.html """
NEW_TABLE_OPTIONS = {
    'minSpareRows': 0,
    'startRows': 4,
    'startCols': 4,
    'colHeaders': False,
    'rowHeaders': True,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo'
    ],
    'editor': 'text',
    'stretchH': 'all',
    'height': 108,
    'renderer': 'text',
    'autoColumnSize': False,
}


class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["flex.FlexPage", "events.ProjectListingPage", "partners.PartnerListingPage", "services.ServiceListingPage", "contact.ContactPage"]
    max_count = 1

    lead_text = models.CharField(
        max_length=140,
        blank=True,
        help_text="Subheading under the banner title",
    )
    button = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        related_name="+",
        help_text="Select an optional page to link to",
        on_delete=models.SET_NULL,
    )
    button_text = models.CharField(
        max_length=50,
        default="Read More",
        blank=False,
        help_text="Button text",
    )
    banner_background_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        help_text="The banner background image.",
        on_delete=models.SET_NULL,
    )
    body = StreamField([
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("image_and_text", blocks.ImageAndTextBlock()),
        ("image", ImageChooserBlock(
            help_text="Ths image will be cropped to 640px by 480px.",
            template="streams/image_block.html"
        )),
        ("cta", blocks.CallToActionBlock()),
        ("testimonial", SnippetChooserBlock(
            target_model="testimonials.Testimonial",
            template="streams/testimonial_block.html"
        )),
        #("pricing_table", blocks.PricingTableBlock(table_options=NEW_TABLE_OPTIONS)),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("lead_text"),
        FieldPanel("button"),
        FieldPanel("button_text"),
        FieldPanel("banner_background_image"),
        FieldPanel("body"),
    ]

    def save(self, *args, **kwargs):

        key = make_template_fragment_key(
            "home_page_streams",
            [self.id],
        )
        cache.delete(key)

        return super().save(*args, **kwargs)
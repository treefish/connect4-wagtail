from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail import blocks as wagtail_blocks
from wagtail.images.blocks import ImageChooserBlock

import flex.models
from streams import blocks
from home.models import NEW_TABLE_OPTIONS


class FlexPage(Page):
    parent_page_types = ["home.HomePage", "flex.FlexPage"]
    body = StreamField([
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("image_and_text", blocks.ImageAndTextBlock()),
        ("cta", blocks.CallToActionBlock()),
        ("testimonial", SnippetChooserBlock(
            target_model="testimonials.Testimonial",
            template="streams/testimonial_block.html"
        )),
        ("pricing_table", blocks.PricingTableBlock(table_options=NEW_TABLE_OPTIONS)),
        #("richtext_with_title", blocks.RichTextWithTitleBlock()),
        ("richtext", wagtail_blocks.RichTextBlock(
            template = "streams/simple_richtext_block.html",
            features = ["bold", "italic", "ol", "ul", "link", "document-link"])
        ),
        ("large_image", ImageChooserBlock(
            help_text = "Ths image will be cropped to 1200px by 775px.",
            template = "streams/large_image_block.html"
        ))
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Flex (misc) page"
        verbose_name_plural = "Flex (misc) pages"
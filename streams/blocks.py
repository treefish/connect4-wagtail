from django import forms
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

class TitleBlock(blocks.StructBlock):
    text = blocks.CharBlock(
        required=True,
        help_text="Text to display",
    )

    class Meta:
        template = "streams/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centered text to display on the page."


class LinkValue(blocks.StructValue):
    """ Additional logic for our links
    """
    def url(self):
        internal_page = self.get("internal_page")
        external_link = self.get("external_link")
        if internal_page:
            return internal_page.url
        elif external_link:
            return external_link
        else:
            return ""


class Link(blocks.StructBlock):

    link_text = blocks.CharBlock(max_length=50, default="More Detail")
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.URLBlock(required=False)

    class Meta:
        value_class = LinkValue

    def clean(self, value):
        internal_page = value.get("internal_page")
        external_link = value.get("external_link")
        errors = {}
        if internal_page and external_link:
            errors["internal_page"] = ErrorList(["Both of these fields cannot be filled. Please select only one option."])
            errors["external_link"] = ErrorList(["Both of these fields cannot be filled. Please select only one option."])
        elif not internal_page and not external_link:
            errors["internal_page"] = ErrorList(["Please select a Page or enter a URL for one of these options."])
            errors["external_link"] = ErrorList(["Please select a Page or enter a URL for one of these options."])

        if errors:
            raise ValidationError("Validation error in your Link", params=errors)

        return super().clean(value)


class Card(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100,
        help_text="Bold title text for this card. Max length of 100 characters.",
    )
    text = blocks.TextBlock(
        max_length=255,
        help_text="Optional text for this card. Max length of 255 characters.",
        required=False,
    )
    image = ImageChooserBlock(
        help_text="Image will be automagically cropped 570px by 370px"
    )
    link = Link(help_text="Enter a URL link or select a page")



class CardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(
        Card()
    )

    class Meta:
        template = "streams/cards_block.html"
        icon = "image"
        label = "Standard Cards"


class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(
            choices=self.field.widget.choices
        )


class ImageAndTextBlock(blocks.StructBlock):

    image = ImageChooserBlock(
        help_text="Image will be automagically cropped to 786px by 552px"
    )
    image_alignment = RadioSelectBlock(
        choices=(
            ("left", "Image to the Left"),
            ("right", "Image to the Right")
        ),
        default="left",
        help_text="Image on the left with text on the right or image on the right with text on the left.",
    )
    title = blocks.CharBlock(
        max_length=60,
        help_text="Max length of 60 characters.",
    )
    text = blocks.CharBlock(
        max_length=60,
        required=False,
    )
    link = Link()

    class Meta:
        template = "streams/image_and_text_block.html"
        icon = "image"
        label = "Image & Text"



class CallToActionBlock(blocks.StructBlock):

    title = blocks.CharBlock(
        max_length=200,
        help_text="Max length of 200 characters.",
    )
    link = Link(help_text="Enter a URL link or select a page")

    class Meta:
        template = "streams/call_to_action_block.html"
        icon = "plus"
        label = "Call to Action"


class PricingTableBlock(TableBlock):

    class Meta:
        template = "streams/pricing_table_block.html"
        icon = "table"
        label = "Pricing"
        help_text = "Your pricing tables should always have four columns."


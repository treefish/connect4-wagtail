from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


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

# Generated by Django 4.2.7 on 2023-11-14 08:10

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0006_remove_eventpage_event_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventpage",
            name="detail",
            field=wagtail.fields.StreamField(
                [
                    (
                        "image_and_text",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        help_text="Image will be automagically cropped to 786px by 552px"
                                    ),
                                ),
                                (
                                    "image_alignment",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("left", "Image to the Left"),
                                            ("right", "Image to the Right"),
                                        ],
                                        help_text="Image on the left with text on the right or image on the right with text on the left.",
                                    ),
                                ),
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Max length of 60 characters.",
                                        max_length=60,
                                    ),
                                ),
                                (
                                    "text",
                                    wagtail.blocks.CharBlock(
                                        max_length=60, required=False
                                    ),
                                ),
                                (
                                    "link",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "link_text",
                                                wagtail.blocks.CharBlock(
                                                    default="More Detail", max_length=50
                                                ),
                                            ),
                                            (
                                                "internal_page",
                                                wagtail.blocks.PageChooserBlock(
                                                    required=False
                                                ),
                                            ),
                                            (
                                                "external_link",
                                                wagtail.blocks.URLBlock(required=False),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "cta",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Max length of 200 characters.",
                                        max_length=200,
                                    ),
                                ),
                                (
                                    "link",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "link_text",
                                                wagtail.blocks.CharBlock(
                                                    default="More Detail", max_length=50
                                                ),
                                            ),
                                            (
                                                "internal_page",
                                                wagtail.blocks.PageChooserBlock(
                                                    required=False
                                                ),
                                            ),
                                            (
                                                "external_link",
                                                wagtail.blocks.URLBlock(required=False),
                                            ),
                                        ],
                                        help_text="Enter a URL link or select a page",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "richtext",
                        wagtail.blocks.RichTextBlock(
                            features=[
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                            template="streams/simple_richtext_block.html",
                        ),
                    ),
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]
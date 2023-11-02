# Generated by Django 4.2.6 on 2023-11-02 22:37

from django.db import migrations
import streams.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0007_alter_homepage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "title",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "text",
                                    wagtail.blocks.CharBlock(
                                        help_text="Text to display", required=True
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "cards",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "cards",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "title",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Bold title text for this card. Max length of 100 characters.",
                                                        max_length=100,
                                                    ),
                                                ),
                                                (
                                                    "text",
                                                    wagtail.blocks.TextBlock(
                                                        help_text="Optional text for this card. Max length of 255 characters.",
                                                        max_length=255,
                                                        required=False,
                                                    ),
                                                ),
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        help_text="Image will be automagically cropped 570px by 370px"
                                                    ),
                                                ),
                                                (
                                                    "link",
                                                    wagtail.blocks.StructBlock(
                                                        [
                                                            (
                                                                "link_text",
                                                                wagtail.blocks.CharBlock(
                                                                    default="More Detail",
                                                                    max_length=50,
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
                                                                wagtail.blocks.URLBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                        ],
                                                        help_text="Enter a URL link or select a page",
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                    ),
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
                    ("image", wagtail.images.blocks.ImageChooserBlock(required=False)),
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
                        "testimonial",
                        wagtail.snippets.blocks.SnippetChooserBlock(
                            target_model="testimonials.Testimonial",
                            template="streams/testimonial_block.html",
                        ),
                    ),
                    (
                        "pricing_table",
                        streams.blocks.PricingTableBlock(
                            table_options={
                                "autoColumnSize": False,
                                "colHeaders": False,
                                "contextMenu": [
                                    "row_above",
                                    "row_below",
                                    "---------",
                                    "col_left",
                                    "col_right",
                                    "---------",
                                    "remove_row",
                                    "remove_col",
                                    "---------",
                                    "undo",
                                    "redo",
                                ],
                                "editor": "text",
                                "height": 108,
                                "minSpareRows": 0,
                                "renderer": "text",
                                "rowHeaders": True,
                                "startCols": 4,
                                "startRows": 4,
                                "stretchH": "all",
                            }
                        ),
                    ),
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-24 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("partners", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnerListingPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("subtitle", models.TextField(blank=True, max_length=500)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PartnerPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("name", models.TextField(max_length=100)),
                ("external_page", models.URLField(blank=True)),
                ("button_text", models.CharField(blank=True, max_length=50)),
                (
                    "internal_page",
                    models.ForeignKey(
                        blank=True,
                        help_text="Select an internal Wagtail page",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "partner_image",
                    models.ForeignKey(
                        help_text="This image will be used on the Partner Listing Page and will be cropped to 570px by 370px on this page.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.DeleteModel(
            name="Partner",
        ),
    ]

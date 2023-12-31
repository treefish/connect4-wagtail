# Generated by Django 4.2.5 on 2023-09-17 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="banner_background_image",
            field=models.ForeignKey(
                help_text="The banner background image.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="button",
            field=models.ForeignKey(
                blank=True,
                help_text="Select an optional page to link to",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.page",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="button_text",
            field=models.CharField(
                default="Read More", help_text="Button text", max_length=50
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="lead_text",
            field=models.CharField(
                blank=True,
                help_text="Subheading under the banner title",
                max_length=140,
            ),
        ),
    ]

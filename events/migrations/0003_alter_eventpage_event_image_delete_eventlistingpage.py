# Generated by Django 4.2.5 on 2023-10-09 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('events', '0002_eventlistingpage_eventpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='event_image',
            field=models.ForeignKey(help_text='This image will be used on the Project Page and will be cropped to 570px by 370px on this page.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.DeleteModel(
            name='EventListingPage',
        ),
    ]
# Generated by Django 4.2.6 on 2023-10-31 21:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0003_eventpage_event_type_list"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventpage",
            name="event_type",
        ),
    ]

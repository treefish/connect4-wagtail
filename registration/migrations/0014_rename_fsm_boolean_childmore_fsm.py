# Generated by Django 4.2.6 on 2023-10-31 23:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("registration", "0013_remove_childmore_fsm_alter_childmore_fsm_boolean"),
    ]

    operations = [
        migrations.RenameField(
            model_name="childmore",
            old_name="fsm_boolean",
            new_name="fsm",
        ),
    ]

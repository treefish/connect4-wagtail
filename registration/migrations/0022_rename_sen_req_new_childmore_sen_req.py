# Generated by Django 4.2.6 on 2023-11-01 02:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("registration", "0021_rename_sen_req_childmore_sen_req_old"),
    ]

    operations = [
        migrations.RenameField(
            model_name="childmore",
            old_name="sen_req_new",
            new_name="sen_req",
        ),
    ]

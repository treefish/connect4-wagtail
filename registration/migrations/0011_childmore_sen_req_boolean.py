# Generated by Django 4.2.6 on 2023-10-31 23:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("registration", "0010_rename_sen_new_childmore_sen_req"),
    ]

    operations = [
        migrations.AddField(
            model_name="childmore",
            name="sen_req_boolean",
            field=models.BooleanField(
                default=False,
                verbose_name="Special educational needs (SEN) or Education health care plan (EHCP)?",
            ),
            preserve_default=False,
        ),
    ]

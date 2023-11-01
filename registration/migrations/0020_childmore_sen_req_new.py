# Generated by Django 4.2.6 on 2023-11-01 02:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("registration", "0019_remove_childmore_fsm_char_childmore_fsm"),
    ]

    operations = [
        migrations.AddField(
            model_name="childmore",
            name="sen_req_new",
            field=models.BooleanField(
                null=True,
                verbose_name="Special educational needs (SEN) or Education health care plan (EHCP)?",
            ),
        ),
    ]

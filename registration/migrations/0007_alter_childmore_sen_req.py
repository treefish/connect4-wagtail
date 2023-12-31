# Generated by Django 4.2.6 on 2023-10-31 22:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("registration", "0006_alter_childmore_fsm_alter_childmore_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="childmore",
            name="sen_req",
            field=models.BooleanField(
                default=False,
                verbose_name="Special educational needs (SEN) or Education health care plan (EHCP)?",
            ),
        ),
    ]

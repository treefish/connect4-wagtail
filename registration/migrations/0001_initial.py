# Generated by Django 4.2.6 on 2023-10-10 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FamilyMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PARENT", "Parent / Caregiver"), ("CHILD", "Child")],
                        default="PARENT",
                        max_length=6,
                        verbose_name="Type",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=100, verbose_name="First name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=100, verbose_name="Last name"),
                ),
                (
                    "diet_req",
                    models.BooleanField(
                        default=False, verbose_name="Dietary requirements?"
                    ),
                ),
                (
                    "diet_detail",
                    models.TextField(
                        blank=True,
                        max_length=1024,
                        null=True,
                        verbose_name="Dietary requirements",
                    ),
                ),
                (
                    "medical_req",
                    models.BooleanField(default=False, verbose_name="Medical needs?"),
                ),
                (
                    "medical_detail",
                    models.TextField(
                        blank=True,
                        max_length=1024,
                        null=True,
                        verbose_name="Medical details",
                    ),
                ),
                (
                    "family",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="family_member",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ParentMore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "family_member",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registration.familymember",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChildMore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dob", models.DateField(verbose_name="Date of Birth")),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("FEMALE", "Female"),
                            ("MALE", "Male"),
                            ("OTHER", "Other"),
                            ("BLANK", "-"),
                        ],
                        default="BLANK",
                        max_length=6,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "school",
                    models.TextField(
                        blank=True, max_length=100, null=True, verbose_name="School"
                    ),
                ),
                (
                    "fsm",
                    models.BooleanField(default=False, verbose_name="Free School Meal"),
                ),
                (
                    "sen_req",
                    models.BooleanField(
                        default=False, verbose_name="SEN Requirements?"
                    ),
                ),
                (
                    "sen_detail",
                    models.TextField(
                        blank=True,
                        max_length=1024,
                        null=True,
                        verbose_name="SEN Requirements",
                    ),
                ),
                (
                    "family_member",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registration.familymember",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Child",
            fields=[],
            options={
                "verbose_name_plural": "Children",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("registration.familymember",),
        ),
        migrations.CreateModel(
            name="Parent",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("registration.familymember",),
        ),
    ]
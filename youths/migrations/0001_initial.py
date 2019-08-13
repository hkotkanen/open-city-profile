# Generated by Django 2.2.3 on 2019-08-13 08:25

from django.db import migrations, models
import django.db.models.deletion
import youths.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("profiles", "0006_add_profile_image")]

    operations = [
        migrations.CreateModel(
            name="YouthProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ssn", models.CharField(max_length=11)),
                ("school_name", models.CharField(max_length=128)),
                ("school_class", models.CharField(max_length=10)),
                (
                    "expiration",
                    models.DateField(default=youths.models.calculate_expiration),
                ),
                (
                    "preferred_language",
                    models.CharField(
                        choices=[
                            ("fi", "Finnish"),
                            ("en", "English"),
                            ("sv", "Swedish"),
                            ("so", "Somali"),
                            ("ar", "Arabic"),
                        ],
                        default="fi",
                        max_length=32,
                    ),
                ),
                ("volunteer_info", models.TextField(blank=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                            ("dont_know", "Don't know"),
                            ("rather_not_say", "Rather not say"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "illnesses",
                    youths.models.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("diabetes", "Diabetes"),
                                ("epilepsy", "Epilepsy"),
                                (
                                    "heart_disease",
                                    "Serious heart or circulatory disease",
                                ),
                                ("serious_allergy", "Serious allergy"),
                            ],
                            max_length=32,
                        ),
                        blank=True,
                        null=True,
                        size=4,
                    ),
                ),
                ("allergies", models.TextField(blank=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.Profile",
                    ),
                ),
            ],
        )
    ]
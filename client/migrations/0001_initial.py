# Generated by Django 4.1.7 on 2023-05-18 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomClient",
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
                ("first_name", models.CharField(max_length=25)),
                ("last_name", models.CharField(max_length=25)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone", models.CharField(max_length=20, unique=True)),
                (
                    "mobile",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                ("company_name", models.CharField(max_length=250)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("is_prospect", models.BooleanField(blank=True, default=True)),
            ],
        ),
    ]
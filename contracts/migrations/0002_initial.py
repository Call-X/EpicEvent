# Generated by Django 4.1.7 on 2023-05-18 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("client", "0002_initial"),
        ("contracts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="support_contact",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"usergroup": "Support"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contract",
            name="client",
            field=models.ForeignKey(
                limit_choices_to={"is_prospect": False},
                on_delete=django.db.models.deletion.CASCADE,
                to="client.customclient",
            ),
        ),
        migrations.AddField(
            model_name="contract",
            name="sales_contact",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"usergroup": "Sale"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

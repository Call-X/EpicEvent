# Generated by Django 4.1.7 on 2023-06-01 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]

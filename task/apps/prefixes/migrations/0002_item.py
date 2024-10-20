# Generated by Django 5.1.2 on 2024-10-17 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prefixes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("name", models.CharField(max_length=255)),
                (
                    "prefix",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="prefixes.prefix",
                    ),
                ),
            ],
        ),
    ]

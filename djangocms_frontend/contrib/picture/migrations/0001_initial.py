# Generated by Django 3.2.11 on 2022-01-13 12:26

from django.db import migrations

import djangocms_frontend.contrib.link.models
import djangocms_frontend.contrib.picture.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("djangocms_frontend", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Picture",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                djangocms_frontend.contrib.link.models.GetLinkMixin,
                djangocms_frontend.contrib.picture.models.ImageMixin,
                "djangocms_frontend.frontenduiitem",
            ),
        ),
    ]

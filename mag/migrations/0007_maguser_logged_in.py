# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-10 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mag', '0006_auto_20171209_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='maguser',
            name='logged_in',
            field=models.BooleanField(default=False),
        ),
    ]

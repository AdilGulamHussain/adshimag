# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-10 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mag', '0007_maguser_logged_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='maguser',
            name='password',
            field=models.CharField(max_length=64, null=True),
        ),
    ]

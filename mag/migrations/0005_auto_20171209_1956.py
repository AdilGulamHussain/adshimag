# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-09 19:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mag', '0004_remove_article_img_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maguser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='maguser',
            name='last_name',
        ),
    ]

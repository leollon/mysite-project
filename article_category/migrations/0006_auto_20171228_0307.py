# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 03:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_category', '0005_auto_20171217_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecategory',
            name='article_number',
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

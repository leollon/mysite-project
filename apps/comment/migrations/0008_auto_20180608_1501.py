# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-08 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0007_auto_20180106_0659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created_time',)},
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='link',
            field=models.URLField(blank=True, max_length=32),
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comments',
        ),
    ]

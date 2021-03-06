# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-25 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20171124_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this user                                     should be treated as active.Unselect this                                     instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user                                                can log into this site', verbose_name='staff'),
        ),
    ]

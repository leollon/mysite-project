# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 03:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article_category', '0001_initial'),
        ('article', '0004_auto_20170607_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article_category.ArticleCategory'),
        ),
    ]

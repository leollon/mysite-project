# Generated by Django 2.2.8 on 2020-01-29 08:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0010_auto_20190117_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

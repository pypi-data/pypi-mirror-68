# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-11 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_history_json_args'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='revision',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='json_args',
            field=models.TextField(default='{}'),
        ),
    ]

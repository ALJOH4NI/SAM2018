# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-30 04:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAM2018', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='authorNmae',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='paper',
            name='contact',
            field=models.CharField(max_length=60, null=True),
        ),
    ]

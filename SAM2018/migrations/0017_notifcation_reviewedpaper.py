# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-03 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAM2018', '0016_auto_20171203_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifcation',
            name='reviewedPaper',
            field=models.CharField(max_length=60, null=True),
        ),
    ]

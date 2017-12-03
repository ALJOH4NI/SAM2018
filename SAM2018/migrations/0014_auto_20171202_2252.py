# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 22:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SAM2018', '0013_auto_20171202_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritepaper',
            name='papers',
        ),
        migrations.AddField(
            model_name='favoritepaper',
            name='papers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SAM2018.Paper'),
        ),
    ]
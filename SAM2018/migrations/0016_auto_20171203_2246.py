# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-03 22:46
from __future__ import unicode_literals

import SAM2018.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAM2018', '0015_notifcation_notiftemp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='uplaod',
            field=models.FileField(null=True, upload_to=b'documents/%Y/%m/%d', validators=[SAM2018.models.validate_file_extension]),
        ),
    ]

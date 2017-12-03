# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 22:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SAM2018', '0011_notifcationtemp'),
    ]

    operations = [
        migrations.CreateModel(
            name='favoritePaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SAM2018.Paper')),
                ('pcm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
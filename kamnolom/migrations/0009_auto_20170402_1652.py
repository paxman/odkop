# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-02 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kamnolom', '0008_auto_20170402_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='izsek',
            name='vsebina',
            field=models.TextField(default='', null=True),
        ),
    ]

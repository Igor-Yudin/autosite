# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-06 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0004_auto_20170428_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteparameters',
            name='age',
            field=models.IntegerField(choices=[(3, '5 - 15'), (2, '15-25'), (1, '25-55')], default=1),
        ),
    ]

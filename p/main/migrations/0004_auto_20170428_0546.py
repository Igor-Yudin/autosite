# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 02:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20170428_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='features',
            name='about_good_type',
            field=models.IntegerField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=0),
        ),
        migrations.AlterField(
            model_name='features',
            name='about_us_type',
            field=models.IntegerField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=0),
        ),
        migrations.AlterField(
            model_name='features',
            name='contacts_type',
            field=models.IntegerField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=0),
        ),
        migrations.AlterField(
            model_name='features',
            name='main_type',
            field=models.IntegerField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=1),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0002_auto_20170428_0102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='features',
            name='about_good_background',
        ),
        migrations.RemoveField(
            model_name='features',
            name='about_us_background',
        ),
        migrations.RemoveField(
            model_name='features',
            name='contacts_background',
        ),
        migrations.RemoveField(
            model_name='features',
            name='main_background',
        ),
        migrations.AddField(
            model_name='features',
            name='about_good_color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
        migrations.AddField(
            model_name='features',
            name='about_good_image',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='features',
            name='about_us_color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
        migrations.AddField(
            model_name='features',
            name='about_us_image',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='features',
            name='contacts_color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
        migrations.AddField(
            model_name='features',
            name='contacts_image',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='features',
            name='main_color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
        migrations.AddField(
            model_name='features',
            name='main_image',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='about_good_type',
            field=models.CharField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='features',
            name='about_us_type',
            field=models.CharField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='features',
            name='contacts_type',
            field=models.CharField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=0, max_length=20),
        ),
    ]

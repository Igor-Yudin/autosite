# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-27 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='features',
            old_name='about_good_header_color',
            new_name='about_good_h_color',
        ),
        migrations.RenameField(
            model_name='features',
            old_name='about_us_header_color',
            new_name='about_us_h_color',
        ),
        migrations.RenameField(
            model_name='features',
            old_name='contacts_header_color',
            new_name='contacts_h_color',
        ),
        migrations.RenameField(
            model_name='features',
            old_name='header_size',
            new_name='h_size',
        ),
        migrations.RenameField(
            model_name='features',
            old_name='main_header_color',
            new_name='main_h_color',
        ),
        migrations.RenameField(
            model_name='features',
            old_name='main_header_size',
            new_name='main_h_size',
        ),
        migrations.RemoveField(
            model_name='siteparameters',
            name='sex',
        ),
        migrations.AddField(
            model_name='siteparameters',
            name='gender',
            field=models.IntegerField(choices=[(2, 'Мужчины'), (3, 'Женщины'), (1, 'Мужчины и женщины')], default=1),
        ),
        migrations.AlterField(
            model_name='features',
            name='about_good_type',
            field=models.CharField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='features',
            name='about_us_type',
            field=models.CharField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='features',
            name='contacts_type',
            field=models.CharField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='features',
            name='main_type',
            field=models.CharField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'Seperate header')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='page',
            name='page_type',
            field=models.IntegerField(choices=[(1, 'Image'), (2, 'Color'), (3, 'Color and image'), (4, 'seperate header')], default=2),
        ),
        migrations.AlterField(
            model_name='siteparameters',
            name='age',
            field=models.IntegerField(choices=[(3, '5 - 15'), (2, '15-25'), (1, '25-55'), (4, '55+')], default=1),
        ),
    ]
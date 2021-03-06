# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-27 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slogan', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('about_good_header', models.CharField(blank=True, max_length=150)),
                ('about_good_text', models.TextField(blank=True)),
                ('about_us_header', models.CharField(blank=True, max_length=150)),
                ('about_us_text', models.TextField(blank=True)),
                ('contacts_header', models.CharField(blank=True, max_length=150)),
                ('contacts_text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('font_family', models.CharField(default='Arial', max_length=250)),
                ('header_size', models.IntegerField(default=25)),
                ('p_size', models.IntegerField(default=12)),
                ('main_type', models.CharField(choices=[('color', 'Color'), ('image', 'Image'), ('color and image', 'Color and image'), ('seperate header', 'Seperate header')], default='color', max_length=20)),
                ('main_background', models.CharField(default='#ffffff', max_length=1000)),
                ('main_header_color', models.CharField(default='black', max_length=30)),
                ('main_header_size', models.IntegerField(default=90)),
                ('main_p_color', models.CharField(default='black', max_length=30)),
                ('main_p_size', models.IntegerField(default=45)),
                ('about_us_type', models.CharField(choices=[('color', 'Color'), ('image', 'Image'), ('color and image', 'Color and image'), ('seperate header', 'Seperate header')], default='color', max_length=20)),
                ('about_us_background', models.CharField(default='#ffffff', max_length=1000)),
                ('about_us_header_color', models.CharField(default='black', max_length=30)),
                ('about_us_p_color', models.CharField(default='black', max_length=30)),
                ('about_good_type', models.CharField(choices=[('color', 'Color'), ('image', 'Image'), ('color and image', 'Color and image'), ('seperate header', 'Seperate header')], default='color', max_length=20)),
                ('about_good_background', models.CharField(default='#ffffff', max_length=1000)),
                ('about_good_header_color', models.CharField(default='black', max_length=30)),
                ('about_good_p_color', models.CharField(default='black', max_length=30)),
                ('contacts_type', models.CharField(choices=[('color', 'Color'), ('image', 'Image'), ('color and image', 'Color and image'), ('seperate header', 'Seperate header')], default='color', max_length=20)),
                ('contacts_background', models.CharField(default='#ffffff', max_length=1000)),
                ('contacts_header_color', models.CharField(default='black', max_length=30)),
                ('contacts_p_color', models.CharField(default='black', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_type', models.IntegerField(choices=[(1, 'Color'), (2, 'Image'), (3, 'Color and image'), (4, 'seperate header')], default=1)),
                ('header', models.CharField(max_length=150)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SiteParameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.TextField()),
                ('sex', models.IntegerField(choices=[(1, 'Мужчины'), (2, 'Женщины'), (3, 'Мужчины и женщины')], default=1)),
                ('age', models.IntegerField(choices=[(1, '5 - 15'), (2, '15-25'), (3, '25-55'), (4, '55+')], default=1)),
            ],
        ),
    ]

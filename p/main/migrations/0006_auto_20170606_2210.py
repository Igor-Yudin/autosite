# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-06 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170606_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='about_good_header',
            field=models.CharField(blank=True, default='h', max_length=150),
        ),
        migrations.AlterField(
            model_name='content',
            name='about_good_text',
            field=models.TextField(blank=True, default='t'),
        ),
        migrations.AlterField(
            model_name='content',
            name='about_us_header',
            field=models.CharField(blank=True, default='h', max_length=150),
        ),
        migrations.AlterField(
            model_name='content',
            name='about_us_text',
            field=models.TextField(blank=True, default='t'),
        ),
        migrations.AlterField(
            model_name='content',
            name='contacts_header',
            field=models.CharField(blank=True, default='h', max_length=150),
        ),
        migrations.AlterField(
            model_name='content',
            name='contacts_text',
            field=models.TextField(blank=True, default='t'),
        ),
        migrations.AlterField(
            model_name='content',
            name='logo',
            field=models.ImageField(blank=True, default='logo.png', null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='content',
            name='name',
            field=models.CharField(default='Name', max_length=100),
        ),
        migrations.AlterField(
            model_name='content',
            name='slogan',
            field=models.TextField(blank=True, default='Slogan'),
        ),
    ]

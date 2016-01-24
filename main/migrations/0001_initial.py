# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-24 05:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_locations', models.TextField(max_length=1000)),
                ('common_nouns', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profiles', models.TextField(max_length=100)),
                ('diseases', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Disease')),
            ],
        ),
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.CharField(max_length=30)),
            ],
        ),
    ]
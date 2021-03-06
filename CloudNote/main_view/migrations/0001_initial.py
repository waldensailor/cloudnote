# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-28 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(null=True)),
                ('create_time', models.DateTimeField(null=True)),
                ('last_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('user_article_id', models.IntegerField()),
                ('tag', models.CharField(max_length=12)),
            ],
        ),
    ]

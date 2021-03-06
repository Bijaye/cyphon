# -*- coding: utf-8 -*-
# Copyright 2017-2018 Dunbar Security Solutions, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.
#
# Generated by Django 1.10.1 on 2017-03-20 16:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datasieves', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_level', models.CharField(choices=[('CRITICAL', 'Critical'), ('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low'), ('INFO', 'Info')], help_text='The Alert level to be returned if the DataSieve returns True for the data examined.', max_length=255)),
                ('rank', models.IntegerField(default=0, help_text='An integer representing the order of this step in the Inspection. Steps are performed in ascending order, with the lowest number examined first.')),
                ('sieve', models.ForeignKey(help_text='The DataSieve used to inspect the data during this step.', on_delete=django.db.models.deletion.CASCADE, related_name='sieves', related_query_name='sieve', to='datasieves.DataSieve')),
            ],
            options={
                'ordering': ['rank'],
            },
        ),
        migrations.CreateModel(
            name='Watchdog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Muzzle',
            fields=[
                ('watchdog', models.OneToOneField(help_text='The Watchdog to be muzzled.', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='watchdogs.Watchdog')),
                ('matching_fields', models.CharField(help_text='A comma-separated string of field names. Defines data fields whose values should be used to identify duplicate Alerts.', max_length=255)),
                ('time_interval', models.PositiveIntegerField(help_text='The length of time within which generation of duplicate Alerts should be supressed.')),
                ('time_unit', models.CharField(choices=[('s', 'Seconds'), ('m', 'Minutes'), ('h', 'Hours'), ('d', 'Days')], help_text='The units of the time interval.', max_length=3)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='watchdog',
            name='categories',
            field=models.ManyToManyField(blank=True, help_text='Restrict coverage to Distilleries with these Categories. If no Categories are selected, all Distilleries will be covered.', related_name='watchdogs', related_query_name='watchdog', to='categories.Category'),
        ),
        migrations.AddField(
            model_name='watchdog',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='Only show Alerts to Users in these Groups. If no Groups are selected, Alerts will be visible to all Groups.', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='trigger',
            name='watchdog',
            field=models.ForeignKey(help_text='The Watchdog with which this trigger is associated.', on_delete=django.db.models.deletion.CASCADE, related_name='triggers', related_query_name='trigger', to='watchdogs.Watchdog', verbose_name='watchdog'),
        ),
        migrations.AlterUniqueTogether(
            name='trigger',
            unique_together=set([('watchdog', 'rank'), ('watchdog', 'sieve')]),
        ),
    ]

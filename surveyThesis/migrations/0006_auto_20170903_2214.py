# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-03 22:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0005_auto_20170903_2153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveyline',
            old_name='readingProblems',
            new_name='hearingProblems',
        ),
        migrations.RenameField(
            model_name='surveyline',
            old_name='readingProblemsDetails',
            new_name='hearingProblemsDetails',
        ),
    ]

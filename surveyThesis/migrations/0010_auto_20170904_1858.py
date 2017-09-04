# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0009_auto_20170904_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foreignlangline',
            old_name='livedAbroad',
            new_name='lived',
        ),
        migrations.RenameField(
            model_name='foreignlangline',
            old_name='livedAbroadDays',
            new_name='livedDays',
        ),
        migrations.RenameField(
            model_name='foreignlangline',
            old_name='livedAbroadDaysTotal',
            new_name='livedDaysTotal',
        ),
        migrations.RenameField(
            model_name='foreignlangline',
            old_name='livedAbroadMonths',
            new_name='livedMonths',
        ),
        migrations.RenameField(
            model_name='foreignlangline',
            old_name='livedAbroadWeeks',
            new_name='livedWeeks',
        ),
        migrations.RenameField(
            model_name='foreignlangline',
            old_name='livedAbroadYears',
            new_name='livedYears',
        ),
    ]

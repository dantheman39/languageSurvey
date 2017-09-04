# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0008_auto_20170904_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='foreignlangline',
            name='livedAbroadDaysTotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='livedAbroadMonths',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='livedAbroadWeeks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='livedAbroadYears',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='otherDaysTotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='otherMonths',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='otherWeeks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='otherYears',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='schoolSemestersTotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='schoolYears',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='workedMonths',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='workedTotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='workedWeeks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='foreignlangline',
            name='workedYears',
            field=models.IntegerField(default=0),
        ),
    ]

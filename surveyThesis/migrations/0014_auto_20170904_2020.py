# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0013_surveyline_datelastedited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyline',
            name='date',
            field=models.DateTimeField(),
        ),
    ]

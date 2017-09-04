# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0011_auto_20170904_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyline',
            name='adminComment',
            field=models.TextField(blank=True),
        ),
    ]

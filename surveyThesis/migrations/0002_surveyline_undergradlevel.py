# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyline',
            name='undergradLevel',
            field=models.CharField(blank=True, max_length=50, choices=[(b'fr', 'Freshman'), (b'sp', 'Sophomore'), (b'jr', 'Junior'), (b'sr', 'Senior')]),
        ),
    ]

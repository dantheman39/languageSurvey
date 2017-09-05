# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0014_auto_20170904_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyline',
            name='gender',
            field=models.CharField(max_length=50, choices=[(b'', b''), (b'f', 'Female'), (b'm', 'Male'), (b'o', 'Other')]),
        ),
    ]

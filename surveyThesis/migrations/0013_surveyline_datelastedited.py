# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0012_surveyline_admincomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyline',
            name='dateLastEdited',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 4, 20, 13, 53, 711136, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]

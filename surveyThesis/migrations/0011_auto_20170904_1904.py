# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveyThesis', '0010_auto_20170904_1858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foreignlangline',
            old_name='workedTotal',
            new_name='workedDaysTotal',
        ),
    ]

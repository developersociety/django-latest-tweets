# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0002_retweeted'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='is_reply',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
    ]

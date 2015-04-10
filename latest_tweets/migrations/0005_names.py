# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0004_username_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tweet',
            name='retweeted_name',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
    ]

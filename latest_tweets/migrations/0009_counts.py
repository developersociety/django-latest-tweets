# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0008_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='favorite_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tweet',
            name='retweet_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

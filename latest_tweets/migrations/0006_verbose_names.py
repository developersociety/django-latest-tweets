# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0005_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='retweeted_tweet_id',
            field=models.BigIntegerField(verbose_name='Retweeted tweet ID', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_id',
            field=models.BigIntegerField(verbose_name='Tweet ID', unique=True),
            preserve_default=True,
        ),
    ]

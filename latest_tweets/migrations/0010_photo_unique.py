# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0009_counts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo_id',
            field=models.BigIntegerField(verbose_name='Photo ID'),
        ),
        migrations.AlterUniqueTogether(
            name='photo',
            unique_together=set([('tweet', 'photo_id')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0007_tweet_html'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('photo_id', models.BigIntegerField(verbose_name='Photo ID', unique=True)),
                ('text', models.CharField(max_length=250)),
                ('text_index', models.PositiveIntegerField(db_index=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('media_url', models.URLField(verbose_name='Media URL')),
                ('large_width', models.PositiveIntegerField()),
                ('large_height', models.PositiveIntegerField()),
                ('tweet', models.ForeignKey(related_name='photos', to='latest_tweets.Tweet')),
            ],
            options={
                'ordering': ('tweet', 'text_index'),
            },
        ),
    ]

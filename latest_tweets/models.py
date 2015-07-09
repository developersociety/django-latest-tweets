from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Tweet(models.Model):
    tweet_id = models.BigIntegerField('Tweet ID', unique=True)
    user = models.CharField(max_length=15, db_index=True)
    name = models.CharField(max_length=20)
    text = models.CharField(max_length=250)
    html = models.TextField('HTML')
    favorite_count = models.PositiveIntegerField(default=0)
    retweet_count = models.PositiveIntegerField(default=0)
    retweeted_username = models.CharField(max_length=20, blank=True)
    retweeted_name = models.CharField(max_length=20, blank=True)
    retweeted_tweet_id = models.BigIntegerField('Retweeted tweet ID', null=True, blank=True)
    is_reply = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '@%s - %s' % (self.user, self.text)

    def get_absolute_url(self):
        return 'https://twitter.com/%s/status/%s' % (self.user, self.tweet_id)

    def user_url(self):
        return 'https://twitter.com/%s' % (self.user,)

    def retweeted_user_url(self):
        if self.retweeted_username:
            return 'https://twitter.com/%s' % (self.retweeted_username,)
        else:
            return None


@python_2_unicode_compatible
class Photo(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='photos')
    photo_id = models.BigIntegerField('Photo ID')
    text = models.CharField(max_length=250)
    text_index = models.PositiveIntegerField(db_index=True)
    url = models.URLField('URL')
    media_url = models.URLField('Media URL')
    large_width = models.PositiveIntegerField()
    large_height = models.PositiveIntegerField()

    class Meta:
        ordering = ('tweet', 'text_index')
        unique_together = (
            ('tweet', 'photo_id'),
        )

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return self.url

    def large_url(self):
        return '%s:large' % (self.media_url,)

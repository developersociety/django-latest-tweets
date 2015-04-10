from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Tweet(models.Model):
    tweet_id = models.BigIntegerField(unique=True)
    user = models.CharField(max_length=15, db_index=True)
    text = models.CharField(max_length=250)
    retweeted_username = models.CharField(max_length=20, blank=True)
    retweeted_tweet_id = models.BigIntegerField(null=True, blank=True)
    is_reply = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '@%s - %s' % (self.user, self.text)

    def get_absolute_url(self):
        return 'https://twitter.com/%s/status/%s' % (self.user, self.tweet_id)

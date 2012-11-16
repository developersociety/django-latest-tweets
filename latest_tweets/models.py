from django.db import models


class Tweet(models.Model):
    tweet_id = models.BigIntegerField(unique=True)
    user = models.CharField(max_length=20, db_index=True)
    text = models.CharField(max_length=250)
    created = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'@%s - %s' % (self.user, self.text)

    def get_absolute_url(self):
        return 'https://twitter.com/%s/status/%s' % (self.user, self.tweet_id)

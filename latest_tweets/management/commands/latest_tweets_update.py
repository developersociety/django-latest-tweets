from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from twitter import OAuth, Twitter

from latest_tweets.models import Tweet
from latest_tweets.utils import update_tweets


@transaction.atomic
def update_user(user):
    t = Twitter(auth=OAuth(
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_SECRET,
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET
    ))
    messages = t.statuses.user_timeline(screen_name=user, include_rts=True)
    tweet_list = update_tweets(messages=messages)

    # To ensure we delete any deleted tweets
    oldest_date = None
    tweet_id_list = []

    for i in tweet_list:
        # Help prune out deleted tweets
        if not oldest_date or i.created < oldest_date:
            oldest_date = i.created

        tweet_id_list.append(i.id)

    # Remove any deleted tweets in our date range
    if oldest_date is not None:
        Tweet.objects.filter(
            user=user, created__gt=oldest_date).exclude(id__in=tweet_id_list).delete()


class Command(BaseCommand):
    args = 'user [user ...]'

    def handle(self, *args, **options):
        for i in args:
            update_user(i)

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.utils.timezone import utc
from datetime import datetime
from twitter import Twitter, OAuth
from latest_tweets.models import Tweet
from django.utils.six.moves import html_parser


@transaction.atomic
def update_user(user):
    t = Twitter(auth=OAuth(
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_SECRET,
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET
    ))
    messages = t.statuses.user_timeline(screen_name=user, include_rts=True)

    # Need to escape HTML entities
    htmlparser = html_parser.HTMLParser()
    unescape = htmlparser.unescape

    # To ensure we delete any deleted tweets
    oldest_date = None
    tweet_id_list = []

    for i in messages:
        tweet_id = i['id']
        tweet_username = i['user']['screen_name']
        tweet_created = datetime.strptime(
            i['created_at'], '%a %b %d %H:%M:%S +0000 %Y'
        ).replace(tzinfo=utc)

        if 'retweeted_status' in i:
            retweeted_username = i['retweeted_status']['user']['screen_name']
            retweeted_tweet_id = i['retweeted_status']['id']
            tweet_text = i['retweeted_status']['text']
        else:
            retweeted_username = ''
            retweeted_tweet_id = None
            tweet_text = i['text']

        tweet_text = unescape(tweet_text)

        obj, created = Tweet.objects.update_or_create(tweet_id=tweet_id, defaults={
            'user': tweet_username,
            'text': tweet_text,
            'retweeted_username': retweeted_username,
            'retweeted_tweet_id': retweeted_tweet_id,
            'created': tweet_created,
        })

        # Help prune out deleted tweets
        if not oldest_date or tweet_created < oldest_date:
            oldest_date = tweet_created

        tweet_id_list.append(obj.id)

    # Remove any deleted tweets in our date range
    Tweet.objects.filter(user=user, created__gt=oldest_date).exclude(id__in=tweet_id_list).delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in args:
            update_user(i)

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from twitter import OAuth, Twitter

from latest_tweets.models import Tweet
from latest_tweets.utils import update_likes, update_tweets


@transaction.atomic
def update_user_tweets(user, download):
    t = Twitter(auth=OAuth(
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_SECRET,
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET
    ))
    messages = t.statuses.user_timeline(screen_name=user, include_rts=True)
    tweet_list = update_tweets(messages=messages, download=download)

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


@transaction.atomic
def update_user_likes(user, download):
    t = Twitter(auth=OAuth(
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_SECRET,
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET
    ))
    messages = t.favorites.list(screen_name=user)
    update_likes(user=user, messages=messages, download=download)


class Command(BaseCommand):
    help = 'Download and store the latest tweets of followed users'

    def add_arguments(self, parser):
        parser.add_argument(
            'users', metavar='user', nargs='+',
            help='Twitter username to update')
        parser.add_argument(
            '--download-photos', action='store_true',
            help='Download images from photos and store locally')
        parser.add_argument(
            '--likes', action='store_true',
            help='Retrieve the list of liked tweets instead of the users tweets')

    def handle(self, **options):
        if options['likes']:
            update_user = update_user_likes
        else:
            update_user = update_user_tweets

        for user in options['users']:
            update_user(user=user, download=options['download_photos'])

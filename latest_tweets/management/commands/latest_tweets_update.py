from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from twitter import OAuth, Twitter
from twitter.api import TwitterHTTPError

from latest_tweets.models import Tweet
from latest_tweets.utils import update_likes, update_tweets


@transaction.atomic
def update_user_tweets(user, download):
    t = Twitter(
        auth=OAuth(
            token=settings.TWITTER_OAUTH_TOKEN,
            token_secret=settings.TWITTER_OAUTH_SECRET,
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
        )
    )
    tweet_list = t.statuses.user_timeline(screen_name=user, include_rts=True)
    tweet_objs = update_tweets(tweet_list=tweet_list, download=download)

    # To ensure we delete any deleted tweets
    oldest_date = None
    tweet_id_list = []

    for tweet in tweet_objs:
        # Help prune out deleted tweets
        if not oldest_date or tweet.created < oldest_date:
            oldest_date = tweet.created

        tweet_id_list.append(tweet.id)

    # Remove any deleted tweets in our date range
    if oldest_date is not None:
        Tweet.objects.filter(user=user, created__gt=oldest_date).exclude(
            id__in=tweet_id_list
        ).delete()


@transaction.atomic
def update_user_likes(user, download):
    t = Twitter(
        auth=OAuth(
            token=settings.TWITTER_OAUTH_TOKEN,
            token_secret=settings.TWITTER_OAUTH_SECRET,
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
        )
    )
    tweet_list = t.favorites.list(screen_name=user)
    update_likes(user=user, tweet_list=tweet_list, download=download)


class Command(BaseCommand):
    help = "Download and store the latest tweets of followed users"

    def add_arguments(self, parser):
        parser.add_argument("users", metavar="user", nargs="+", help="Twitter username to update")
        parser.add_argument(
            "--download-photos",
            action="store_true",
            help="Download images from photos and store locally",
        )
        parser.add_argument(
            "--likes",
            action="store_true",
            help="Retrieve the list of liked tweets instead of the users tweets",
        )

    def handle(self, **options):
        if options["likes"]:
            update_user = update_user_likes
        else:
            update_user = update_user_tweets

        for user in options["users"]:
            try:
                update_user(user=user, download=options["download_photos"])
            except TwitterHTTPError as http_error:
                # Fail quietly on any temporary server error codes. This should avoid raising
                # exceptions when Twitter has temporary HTTP server problems, but network/DNS
                # issues should still reraise an exception as that could be an error on our side.
                if http_error.e.code in (500, 502, 503, 504):
                    self.stderr.write(
                        "Update failed for {} (HTTP {})".format(user, http_error.e.code),
                    )
                else:
                    raise

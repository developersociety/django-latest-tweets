import django

__version__ = "0.4.7"


if django.VERSION < (3, 2):
    default_app_config = "latest_tweets.apps.LatestTweetsConfig"

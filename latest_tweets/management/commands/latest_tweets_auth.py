from django.core.management.base import BaseCommand
from django.conf import settings
from twitter.oauth_dance import oauth_dance


def get_auth_tokens(stdout):
    oauth_token, oauth_secret = oauth_dance(
        'django-latest-tweets', settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)

    stdout.write("\nNow add the following lines to your settings.py:\n\n")
    stdout.write("TWITTER_OAUTH_TOKEN = '%s'\n" % (oauth_token,))
    stdout.write("TWITTER_OAUTH_SECRET = '%s'\n\n" % (oauth_secret,))


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_auth_tokens(self.stdout)

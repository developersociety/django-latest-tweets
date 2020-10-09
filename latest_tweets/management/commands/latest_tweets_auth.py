from django.conf import settings
from django.core.management.base import BaseCommand

from twitter.oauth_dance import oauth_dance


def get_auth_tokens(stdout):
    oauth_token, oauth_secret = oauth_dance(
        app_name="django-latest-tweets",
        consumer_key=settings.TWITTER_CONSUMER_KEY,
        consumer_secret=settings.TWITTER_CONSUMER_SECRET,
    )

    stdout.write("\nNow add the following lines to your settings.py:\n\n")
    stdout.write("TWITTER_OAUTH_TOKEN = '%s'\n" % (oauth_token,))
    stdout.write("TWITTER_OAUTH_SECRET = '%s'\n\n" % (oauth_secret,))


class Command(BaseCommand):
    help = "Generate OAuth tokens/secret needed for Twitter"

    def handle(self, **options):
        get_auth_tokens(self.stdout)

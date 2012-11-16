from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from datetime import datetime
from twitter import Twitter
from latest_tweets.models import Tweet


def update_user(user):
    t = Twitter()
    messages = t.statuses.user_timeline(screen_name=user, include_rts=True)

    for i in messages:
        tweet_id = i['id']
        tweet_username = i['user']['screen_name']
        tweet_text = i['text']
        tweet_created = datetime.strptime(i['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=utc)

        obj, created = Tweet.objects.get_or_create(tweet_id=tweet_id, defaults={
            'user': tweet_username,
            'text': tweet_text,
            'created': tweet_created,
        })


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in args:
            update_user(i)

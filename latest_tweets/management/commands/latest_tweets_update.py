from django.core.management.base import BaseCommand
from datetime import datetime
from twitter import Twitter
from latest_tweets.models import Tweet


def update_user(user):
    t = Twitter()
    messages = t.statuses.user_timeline(screen_name=user, include_rts=True)

    for i in messages:
        obj, created = Tweet.objects.get_or_create(tweet_id=i['id'], defaults={
            'user': i['user']['screen_name'],
            'text': i['text'],
            'created': datetime.strptime(i['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
        })


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in args:
            update_user(i)

from django import template
from latest_tweets.models import Tweet

register = template.Library()


@register.assignment_tag
def get_latest_tweets(user, amount=None):
    tweets = Tweet.objects.filter(user=user)

    if amount is not None:
        tweets = tweets[:amount]

    return tweets

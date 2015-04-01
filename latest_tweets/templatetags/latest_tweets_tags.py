from django import template
from latest_tweets.models import Tweet

register = template.Library()


@register.assignment_tag
def get_latest_tweets(*args, **kwargs):
    limit = kwargs.pop('limit', None)
    tweets = Tweet.objects.all()

    if args:
        tweets = tweets.filter(user__in=args)

    if limit is not None:
        tweets = tweets[:limit]

    return tweets

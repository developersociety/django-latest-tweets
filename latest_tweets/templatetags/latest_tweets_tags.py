from django import template
from latest_tweets.models import Tweet

register = template.Library()


@register.assignment_tag
def get_latest_tweets(*args, **kwargs):
    limit = kwargs.pop('limit', None)
    include_replies = kwargs.pop('include_replies', False)
    liked_by = kwargs.pop('liked_by', None)
    tweets = Tweet.objects.all()

    #  By default we exclude replies
    if not include_replies:
        tweets = tweets.exclude(is_reply=True)

    if liked_by:
        tweets = tweets.filter(like__user=liked_by)

    if args:
        tweets = tweets.filter(user__in=args)

    if limit is not None:
        tweets = tweets[:limit]

    return tweets

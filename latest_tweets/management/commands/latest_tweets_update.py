from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.utils.timezone import utc
from datetime import datetime
from twitter import Twitter, OAuth
from latest_tweets.models import Tweet
from django.utils.six.moves import html_parser


HASHTAG_HTML = '<a href="https://twitter.com/hashtag/{text}" target="_blank">#{text}</a>'
URL_HTML = '<a href="{expanded_url}" target="_blank">{display_url}</a>'
MENTION_HTML = '<a href="https://twitter.com/{screen_name}" target="_blank">@{screen_name}</a>'
SYMBOL_HTML = '<a href="https://twitter.com/search?q=%24{text}" target="_blank">${text}</a>'


def tweet_html_entities(tweet, **kwargs):
    text = list(tweet)

    for hashtag in kwargs.get('hashtags', []):
        start, end = hashtag['indices']
        text[start] = HASHTAG_HTML.format(**hashtag)
        text[start + 1:end] = [''] * (end - start - 1)

    for url in kwargs.get('urls', []):
        start, end = url['indices']
        text[start] = URL_HTML.format(**url)
        text[start + 1:end] = [''] * (end - start - 1)

    for mention in kwargs.get('user_mentions', []):
        start, end = mention['indices']
        text[start] = MENTION_HTML.format(**mention)
        text[start + 1:end] = [''] * (end - start - 1)

    for symbol in kwargs.get('symbols', []):
        start, end = symbol['indices']
        text[start] = SYMBOL_HTML.format(**symbol)
        text[start + 1:end] = [''] * (end - start - 1)

    for media in kwargs.get('media', []):
        start, end = media['indices']
        text[start] = URL_HTML.format(**media)
        text[start + 1:end] = [''] * (end - start - 1)

    return ''.join(text)


@transaction.atomic
def update_user(user):
    t = Twitter(auth=OAuth(
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_SECRET,
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET
    ))
    messages = t.statuses.user_timeline(screen_name=user, include_rts=True)

    # Need to escape HTML entities
    htmlparser = html_parser.HTMLParser()
    unescape = htmlparser.unescape

    # To ensure we delete any deleted tweets
    oldest_date = None
    tweet_id_list = []

    for i in messages:
        tweet_id = i['id']
        tweet_username = i['user']['screen_name']
        tweet_name = i['user']['name']
        tweet_created = datetime.strptime(
            i['created_at'], '%a %b %d %H:%M:%S +0000 %Y'
        ).replace(tzinfo=utc)
        tweet_is_reply = i['in_reply_to_screen_name'] is not None

        if 'retweeted_status' in i:
            retweeted_username = i['retweeted_status']['user']['screen_name']
            retweeted_name = i['retweeted_status']['user']['name']
            retweeted_tweet_id = i['retweeted_status']['id']
            tweet_text = i['retweeted_status']['text']
            tweet_html = tweet_html_entities(tweet_text, **i['retweeted_status']['entities'])
        else:
            retweeted_username = ''
            retweeted_name = ''
            retweeted_tweet_id = None
            tweet_text = i['text']
            tweet_html = tweet_html_entities(tweet_text, **i['entities'])

        tweet_text = unescape(tweet_text)

        obj, created = Tweet.objects.update_or_create(tweet_id=tweet_id, defaults={
            'user': tweet_username,
            'name': tweet_name,
            'text': tweet_text,
            'html': tweet_html,
            'retweeted_username': retweeted_username,
            'retweeted_name': retweeted_name,
            'retweeted_tweet_id': retweeted_tweet_id,
            'is_reply': tweet_is_reply,
            'created': tweet_created,
        })

        # Help prune out deleted tweets
        if not oldest_date or tweet_created < oldest_date:
            oldest_date = tweet_created

        tweet_id_list.append(obj.id)

    # Remove any deleted tweets in our date range
    Tweet.objects.filter(user=user, created__gt=oldest_date).exclude(id__in=tweet_id_list).delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in args:
            update_user(i)

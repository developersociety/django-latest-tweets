import hashlib
from datetime import datetime
from html import unescape
from tempfile import TemporaryFile

from django.core.files import File
from django.utils.timezone import utc

import requests
from PIL import Image

from .models import Hashtag, Like, Photo, Tweet

HASHTAG_HTML = '<a href="https://twitter.com/hashtag/{text}" target="_blank">#{text}</a>'
URL_HTML = '<a href="{expanded_url}" target="_blank">{display_url}</a>'
MENTION_HTML = '<a href="https://twitter.com/{screen_name}" target="_blank">@{screen_name}</a>'
SYMBOL_HTML = '<a href="https://twitter.com/search?q=%24{text}" target="_blank">${text}</a>'


def tweet_html_entities(tweet, **kwargs):
    text = list(tweet)

    for hashtag in kwargs.get("hashtags", []):
        start, end = hashtag["indices"]
        text[start] = HASHTAG_HTML.format(**hashtag)
        text[start + 1 : end] = [""] * (end - start - 1)

    for url in kwargs.get("urls", []):
        start, end = url["indices"]
        text[start] = URL_HTML.format(**url)
        text[start + 1 : end] = [""] * (end - start - 1)

    for mention in kwargs.get("user_mentions", []):
        start, end = mention["indices"]
        text[start] = MENTION_HTML.format(**mention)
        text[start + 1 : end] = [""] * (end - start - 1)

    for symbol in kwargs.get("symbols", []):
        start, end = symbol["indices"]
        text[start] = SYMBOL_HTML.format(**symbol)
        text[start + 1 : end] = [""] * (end - start - 1)

    for media in kwargs.get("media", []):
        start, end = media["indices"]
        text[start] = URL_HTML.format(**media)
        text[start + 1 : end] = [""] * (end - start - 1)

    return "".join(text)


def tweet_hashtags(tweet, hashtags):
    for hashtag in hashtags:
        text = hashtag["text"].lower()

        tag, created = Hashtag.objects.get_or_create(text=text)

        tweet.hashtags.add(tag)


def tweet_photos(tweet, media, download):
    for photo in media:
        # Only photos
        if photo["type"] != "photo":
            continue

        photo_id = photo["id"]
        large = photo["sizes"]["large"]

        obj, created = Photo.objects.get_or_create(
            tweet=tweet,
            photo_id=photo_id,
            defaults={
                "text": photo["display_url"],
                "text_index": photo["indices"][0],
                "url": photo["url"],
                "media_url": photo["media_url_https"],
                "large_width": int(large["w"]),
                "large_height": int(large["h"]),
            },
        )

        if download and not obj.image_file:
            with TemporaryFile() as temp_file:
                image_file = File(temp_file)

                # Download the file
                r = requests.get(obj.media_url, stream=True)
                r.raise_for_status()

                for chunk in r.iter_content(4096):
                    image_file.write(chunk)

                # Get Pillow to look at it
                image_file.seek(0)
                pil_image = Image.open(image_file)
                image_name = "%s.%s" % (
                    hashlib.md5(obj.media_url.encode()).hexdigest(),
                    pil_image.format.lower(),
                )

                # Save the file
                image_file.seek(0)
                obj.image_file.save(image_name, image_file, save=True)


def update_tweets(tweet_list, tweet_entities=tweet_html_entities, download=False):
    obj_list = []

    for tweet in tweet_list:
        tweet_id = tweet["id"]
        tweet_username = tweet["user"]["screen_name"]
        tweet_name = tweet["user"]["name"]
        tweet_created = datetime.strptime(
            tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y"
        ).replace(tzinfo=utc)
        tweet_is_reply = tweet["in_reply_to_screen_name"] is not None

        if "retweeted_status" in tweet:
            retweeted_username = tweet["retweeted_status"]["user"]["screen_name"]
            retweeted_name = tweet["retweeted_status"]["user"]["name"]
            retweeted_tweet_id = tweet["retweeted_status"]["id"]
            tweet_text = tweet["retweeted_status"]["text"]
            tweet_html = tweet_entities(tweet_text, **tweet["retweeted_status"]["entities"])
            favorite_count = tweet["retweeted_status"]["favorite_count"]
            retweet_count = tweet["retweeted_status"]["retweet_count"]
        else:
            retweeted_username = ""
            retweeted_name = ""
            retweeted_tweet_id = None
            tweet_text = tweet["text"]
            tweet_html = tweet_entities(tweet_text, **tweet["entities"])
            favorite_count = tweet["favorite_count"]
            retweet_count = tweet["retweet_count"]

        tweet_text = unescape(tweet_text)

        obj, created = Tweet.objects.get_or_create(
            tweet_id=tweet_id,
            defaults={
                "user": tweet_username,
                "name": tweet_name,
                "text": tweet_text,
                "html": tweet_html,
                "favorite_count": favorite_count,
                "retweet_count": retweet_count,
                "retweeted_username": retweeted_username,
                "retweeted_name": retweeted_name,
                "retweeted_tweet_id": retweeted_tweet_id,
                "is_reply": tweet_is_reply,
                "created": tweet_created,
            },
        )

        if created:
            # Add hashtags
            tweet_hashtags(tweet=obj, hashtags=tweet["entities"].get("hashtags", []))

            # Add any photos
            tweet_photos(tweet=obj, media=tweet["entities"].get("media", []), download=download)
        else:
            # Update counts, but try to avoid excessive updates
            update_fields = []

            if obj.favorite_count != favorite_count:
                obj.favorite_count = favorite_count
                update_fields.append("favorite_count")

            if obj.retweet_count != retweet_count:
                obj.retweet_count = retweet_count
                update_fields.append("retweet_count")

            if update_fields:
                obj.save(update_fields=update_fields)

        obj_list.append(obj)

    return obj_list


def update_likes(user, tweet_list, download=False):
    obj_list = update_tweets(tweet_list=tweet_list, download=download)

    for tweet in obj_list:
        Like.objects.get_or_create(user=user, tweet=tweet)

    return obj_list

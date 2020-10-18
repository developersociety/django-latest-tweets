from django.test import TestCase
from django.utils import timezone

from latest_tweets.models import Hashtag, Tweet


class HashtagTest(TestCase):
    def test_create(self):
        obj = Hashtag.objects.create(text="HashTag")
        self.assertIsNotNone(obj.id)

    def test_str(self):
        obj = Hashtag(text="HashTag")
        self.assertEqual(str(obj), "HashTag")

    def test_get_absolute_url(self):
        obj = Hashtag(text="HashTag")
        self.assertEqual(obj.get_absolute_url(), "https://twitter.com/hashtag/HashTag")


class TweetTest(TestCase):
    def test_create(self):
        obj = Tweet.objects.create(tweet_id=123, created=timezone.now())
        self.assertIsNotNone(obj.id)

    def test_str(self):
        obj = Tweet(tweet_id=123, user="Alice", text="Hello World", created=timezone.now())
        self.assertEqual(str(obj), "@Alice - Hello World")

    def test_get_absolute_url(self):
        obj = Tweet(tweet_id=123, user="Alice", created=timezone.now())
        self.assertEqual(obj.get_absolute_url(), "https://twitter.com/Alice/status/123")

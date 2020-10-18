from django.test import TestCase

from latest_tweets.utils import tweet_html_entities


class TweetHTMLEntitiesTest(TestCase):
    def test_text_only(self):
        tweet_html = tweet_html_entities(tweet="Hello world")

        self.assertEqual(tweet_html, "Hello world")

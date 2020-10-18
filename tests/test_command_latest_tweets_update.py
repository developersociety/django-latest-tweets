from unittest import mock

from django.core.management import call_command
from django.test import TestCase


class LatestTweetsUpdateTest(TestCase):
    @mock.patch("twitter.api.TwitterCall.__call__")
    def test_command(self, mock_twitter_call):
        mock_twitter_call.return_value = []

        result = call_command("latest_tweets_update", "demo")

        self.assertIsNone(result)

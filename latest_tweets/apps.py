from django.apps import AppConfig


class LatestTweetsConfig(AppConfig):
    name = "latest_tweets"
    label = "latest_tweets"
    verbose_name = "Latest Tweets"
    default_auto_field = "django.db.models.AutoField"

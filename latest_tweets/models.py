from django.db import models


class Hashtag(models.Model):
    text = models.CharField(max_length=140, unique=True)

    class Meta:
        ordering = ("text",)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return "https://twitter.com/hashtag/{}".format(self.text)


class Tweet(models.Model):
    tweet_id = models.BigIntegerField("Tweet ID", unique=True)
    user = models.CharField(max_length=15, db_index=True)
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=250)
    html = models.TextField("HTML")
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    favorite_count = models.PositiveIntegerField(default=0)
    retweet_count = models.PositiveIntegerField(default=0)
    retweeted_username = models.CharField(max_length=20, blank=True)
    retweeted_name = models.CharField(max_length=50, blank=True)
    retweeted_tweet_id = models.BigIntegerField("Retweeted tweet ID", null=True, blank=True)
    is_reply = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "@{} - {}".format(self.user, self.text)

    def get_absolute_url(self):
        return "https://twitter.com/{}/status/{}".format(self.user, self.tweet_id)

    def user_url(self):
        return "https://twitter.com/{}".format(self.user)

    def retweeted_user_url(self):
        if self.retweeted_username:
            return "https://twitter.com/{}".format(self.retweeted_username)
        else:
            return None


class Photo(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="photos")
    photo_id = models.BigIntegerField("Photo ID")
    text = models.CharField(max_length=250)
    text_index = models.PositiveIntegerField(db_index=True)
    url = models.URLField("URL")
    media_url = models.URLField("Media URL")
    large_width = models.PositiveIntegerField()
    large_height = models.PositiveIntegerField()
    image_file = models.ImageField(upload_to="latest_tweets/photo", blank=True)

    class Meta:
        ordering = ("tweet", "text_index")
        unique_together = (("tweet", "photo_id"),)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return self.url

    def large_url(self):
        return "{}:large".format(self.media_url)


class Like(models.Model):
    user = models.CharField(max_length=15)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-tweet",)
        unique_together = (("user", "tweet"),)

    def __str__(self):
        return str(self.tweet)

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0003_tweet_is_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='user',
            field=models.CharField(db_index=True, max_length=15),
            preserve_default=True,
        ),
    ]

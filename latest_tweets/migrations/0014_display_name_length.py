from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0013_hashtags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='retweeted_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0012_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('text', models.CharField(unique=True, max_length=140)),
            ],
            options={
                'ordering': ('text',),
            },
        ),
        migrations.AddField(
            model_name='tweet',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='latest_tweets.Hashtag'),
        ),
    ]

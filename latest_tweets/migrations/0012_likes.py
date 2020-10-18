from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0011_photo_image_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('user', models.CharField(max_length=15)),
                ('tweet', models.ForeignKey(to='latest_tweets.Tweet', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('-tweet',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('user', 'tweet')]),
        ),
    ]

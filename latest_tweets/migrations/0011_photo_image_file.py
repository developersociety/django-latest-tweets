from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0010_photo_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image_file',
            field=models.ImageField(blank=True, upload_to='latest_tweets/photo'),
        ),
    ]

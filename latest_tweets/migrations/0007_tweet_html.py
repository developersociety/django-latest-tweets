from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_tweets', '0006_verbose_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='html',
            field=models.TextField(default='', verbose_name='HTML'),
            preserve_default=False,
        ),
    ]

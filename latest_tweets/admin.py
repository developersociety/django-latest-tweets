from django.contrib import admin
from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created')
    list_filter = ('created', 'user')
    date_hierarchy = 'created'
    readonly_fields = (
        'tweet_id', 'user', 'name', 'text', 'tweet_html', 'retweeted_username', 'retweeted_name',
        'retweeted_tweet_id', 'is_reply', 'created')
    fieldsets = (
        (None, {
            'fields': readonly_fields,
        }),
    )

    def has_add_permission(self, request):
        return False

    def tweet_html(self, obj):
        return obj.html
    tweet_html.short_description = 'HTML'
    tweet_html.allow_tags = True

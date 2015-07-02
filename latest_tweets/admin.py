from django.contrib import admin

from .models import Photo, Tweet


class PhotoInline(admin.StackedInline):
    model = Photo
    readonly_fields = ('photo_id', 'url', 'media_url', 'large_width', 'large_height')
    fieldsets = (
        (None, {
            'fields': readonly_fields,
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created')
    list_filter = ('created', 'user')
    date_hierarchy = 'created'
    readonly_fields = (
        'tweet_id', 'user', 'name', 'text', 'tweet_html', 'favorite_count', 'retweet_count',
        'retweeted_username', 'retweeted_name', 'retweeted_tweet_id', 'is_reply', 'created')
    fieldsets = (
        (None, {
            'fields': readonly_fields,
        }),
    )
    inlines = [PhotoInline]

    def has_add_permission(self, request):
        return False

    def tweet_html(self, obj):
        return obj.html
    tweet_html.short_description = 'HTML'
    tweet_html.allow_tags = True

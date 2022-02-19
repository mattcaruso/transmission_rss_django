from django.db import models
from django.forms import ModelForm


class Feed(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True, verbose_name='RSS URL')
    created = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(null=True)
    save_location = models.CharField(unique=True, max_length=1000, verbose_name='Download Path')
    keyword = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title


class FeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = ['title', 'url', 'save_location', 'keyword']


class FeedItem(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    magnet_link = models.URLField()
    uuid = models.CharField(max_length=50, unique=True)
    matched = models.BooleanField(default=False)
    seen = models.DateTimeField(auto_now_add=True)
    sent_to_transmission = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def matches_feed_keyword(self) -> bool:
        return self.feed.keyword in self.title

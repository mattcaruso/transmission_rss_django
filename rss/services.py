import feedparser
import requests
from datetime import datetime as dt
from transmissionrpc import Client

from .models import Feed, FeedItem
from transmission_rss_django.settings import env

RSS_HEADERS = {'User-Agent': 'Mozilla/5.0'}


# TODO Delete this
def test_task():
    print('ping!!')


def check_feeds():
    feeds = Feed.objects.all()

    for feed in feeds:
        load_new_items(feed)

    send_to_transmission()


def load_new_items(feed: Feed):
    """Checks a feed for new items and stores any new items in the db."""

    feed_items = [fi.uuid for fi in FeedItem.objects.all()]

    response = requests.get(feed.url, headers=RSS_HEADERS)
    # TODO Raise exception for a feed URL not returning content

    f = feedparser.parse(response.content)

    for entry in f.entries:

        if entry.id not in feed_items:

            new_feed_item = FeedItem(
                feed=feed,
                title=entry.title,
                magnet_link=entry.link,
                uuid=entry.id
            )
            new_feed_item.matched = new_feed_item.matches_feed_keyword()
            new_feed_item.save()

    feed.last_checked = dt.now()
    feed.save()


def send_to_transmission():

    feed_items = FeedItem.objects.filter(matched=True, sent_to_transmission=False)

    tc = Client(env('TRANSMISSION_ADDRESS'), port=env('TRANSMISSION_PORT'))

    for feed_item in feed_items:
        tc.add_torrent(feed_item.magnet_link, download_dir=env('DOWNLOAD_PATH') + feed_item.feed.save_location)
        feed_item.sent_to_transmission = True
        feed_item.save()

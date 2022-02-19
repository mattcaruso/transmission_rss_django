from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .models import Feed, FeedForm, FeedItem


class IndexView(generic.ListView):
    template_name = 'rss/index.html'
    context_object_name = 'all_feeds'

    def get_queryset(self):
        return Feed.objects.all()


def detail(request, feed_id=None):

    if feed_id:
        feed = get_object_or_404(Feed, pk=feed_id)
    else:
        feed = None

    if request.method == 'POST':
        form = FeedForm(request.POST, instance=feed)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))

    else:
        form = FeedForm(instance=feed)

    return render(request, 'rss/detail.html', {'feed': feed, 'form': form})

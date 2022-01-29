from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .tasks import scrape
from .models import NewsItem


def scrape_page(request):
    URL = "https://dev.to/latest"
    scrape.delay(URL)
    return HttpResponse("Done")


class NewsListView(generic.ListView):
    template_name = "news_list.html"
    paginate_by = 15

    def get_queryset(self):
        qs = NewsItem.objects.all()

        title = self.request.GET.get('title', None)
        if title:
            qs = qs.filter(title__icontains=title)

        return qs.order_by("-publish_date")

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        count = NewsItem.objects.all().count()
        context.update({
            "total_count": count
        })
        return context

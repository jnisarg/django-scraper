from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from .models import NewsItem
from .tasks import scrape_dev_to_task, scrape_hacker_news_task


def news_list_ordering(request, qs):
    source = request.GET.get("source", None)
    author = request.GET.get("author", None)
    title = request.GET.get("title", None)
    date = request.GET.get("date", None)

    if source:
        qs = qs.order_by(
            "-source") if source == "desc" else qs.order_by("source")
    elif author:
        qs = qs.order_by(
            "-author") if author == "desc" else qs.order_by("author")
    elif title:
        qs = qs.order_by(
            "-title") if title == "desc" else qs.order_by("title")
    elif date:
        qs = qs.order_by(
            "-publish_date") if date == "desc" else qs.order_by("publish_date")
    else:
        qs = qs.order_by("-created")

    return qs


def news_list_view(request):
    query = request.GET.get("q", None)
    page_number = request.GET.get("page")
    articles = NewsItem.objects.all()

    if not articles.count():
        scrape_hacker_news_task.delay()
        scrape_dev_to_task.delay()

    if query:
        articles = articles.search(query)

    articles = news_list_ordering(request, articles)
    paginator = Paginator(articles, 15)
    
    context = {
        "object_list": paginator.get_page(page_number),
        "total_count": articles.count(),
    }
    return render(request, "news_list.html", context)

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import NewsItem


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

    # if source:
    #     articles = articles.source(source)
    if query:
        articles = articles.search(query)

    articles = news_list_ordering(request, articles)

    paginator = Paginator(articles, 15)

    context = {
        "object_list": paginator.get_page(page_number),
        # "sources": NewsItem().get_sources(),
        "total_count": articles.count(),
        # "dev_to_count": articles.source("Dev.to").count(),
        # "hn_count": articles.source("HackerNews").count(),
    }
    return render(request, "news_list.html", context)

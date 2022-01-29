from django.urls import path

from .views import NewsListView


app_name = "core"
urlpatterns = [
    # path('', scrape_page),
    path("", NewsListView.as_view(), name="news_list"),
]

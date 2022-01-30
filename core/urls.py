from django.urls import path

from .views import news_list_view


app_name = "core"
urlpatterns = [
    path("", news_list_view, name="news_list"),
]

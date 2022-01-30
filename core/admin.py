from django.contrib import admin

from .models import NewsItem


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("source", "author", "title", "publish_date")
    list_display_links = ("title",)
    list_filter = ("source", "publish_date")
    search_fields = ("title", "author")
    list_per_page = 50
    date_hierarchy = "publish_date"

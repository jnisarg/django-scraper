from django.db import models
from django.db.models import Q


class NewsItemQuerySet(models.QuerySet):
    def search(self, query):
        return self.filter(Q(title__icontains=query) |
                           Q(author__icontains=query) |
                           Q(source__icontains=query))


class NewsItemManager(models.Manager):
    def get_queryset(self):
        return NewsItemQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class NewsItem(models.Model):
    source = models.CharField(max_length=255)
    link = models.TextField()
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    publish_date = models.DateField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = NewsItemManager()

    def __str__(self):
        return f"{self.source}-{self.title}"

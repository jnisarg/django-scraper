from django.db import models
from django.db.models import Q


class NewsItemQuerySet(models.QuerySet):
    def search(self, query):
        return self.filter(Q(title__icontains=query) |
                           Q(author__icontains=query) |
                           Q(source__icontains=query))

    # def source(self, source):
    #     if source in self.model.SourceChoices:
    #         return self.filter(source=source)
    #     return self.all()


class NewsItemManager(models.Manager):
    def get_queryset(self):
        return NewsItemQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    # def source(self, source):
    #     return self.get_queryset().source(source)


class NewsItem(models.Model):

    # class SourceChoices(models.TextChoices):
    #     DEV = "Dev.to", "Dev.to"
    #     HN = "HackerNews", "HackerNews"

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

    # def get_sources(self):
    #     return self.SourceChoices.choices

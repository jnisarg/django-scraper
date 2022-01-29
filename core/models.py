from django.db import models


class NewsItem(models.Model):
    source = models.CharField(max_length=10, choices=(
        ("dev.to", "Dev.to"),
        ("medium", "Medium"),
        ("hn", "HackerNews"),
    ))
    link = models.TextField()
    title = models.CharField(max_length=255)
    publish_date = models.DateField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source}-{self.title}"

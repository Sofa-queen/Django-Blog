"""Файл для хранения QuerySets приложения"""

from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):

    def with_related_data(self):
        return self.select_related(
            'category', 'author', 'location'
        )

    def published(self):
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=timezone.now()
        )

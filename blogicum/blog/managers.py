"""Файл для хранения Manager приложения"""

from django.db import models

from blog.querysets import PostQuerySet


class FilterPostManager(models.Manager):
    def get_queryset(self):
        return (
            PostQuerySet(self.model)
            .with_related_data()
            .published()
        )

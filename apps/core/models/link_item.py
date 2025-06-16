from django.db import models
from django.core.validators import URLValidator


class LinkItem(models.Model):
    """Links collection for link-type notes"""
    note = models.ForeignKey(
        'Note',
        on_delete=models.CASCADE,
        related_name='links'
    )
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    description = models.TextField(blank=True)
    favicon_url = models.URLField(blank=True, null=True)  # for link icons
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Link Item"
        verbose_name_plural = "Link Items"

    def __str__(self):
        return f"{self.title} - {self.url}"

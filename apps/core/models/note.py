from django.db import models
from django.conf import settings


class Note(models.Model):
    """Main note model with different types"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    NOTE_TYPE_CHOICES = [
        ('text', 'Text Note'),
        ('checklist', 'Checklist'),
        ('table', 'Table'),
        ('drawing', 'Drawing/Sketch'),
        ('voice', 'Voice Note'),
        ('link', 'Link Collection'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)  # for text notes
    board = models.ForeignKey(
        'Board',
        on_delete=models.CASCADE,
        related_name='notes')
    note_type = models.CharField(
        max_length=20,
        choices=NOTE_TYPE_CHOICES,
        default='text'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notes'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return f"{self.title} ({self.get_note_type_display()}) by {self.author.username}"
    
import os
from django.db import models


def note_attachment_path(instance, filename):
    """Generate upload path for note attachments"""
    return f'attachments/notes/{instance.note.id}/{filename}'


class Attachment(models.Model):
    """File attachments for notes"""
    note = models.ForeignKey(
        'Note',
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to=note_attachment_path)
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # size in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.original_filename} ({self.note.title})"

    def save(self, *args, **kwargs):
        if self.file:
            self.original_filename = self.file.name
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    @property
    def file_extension(self):
        return os.path.splitext(self.original_filename)[1].lower()

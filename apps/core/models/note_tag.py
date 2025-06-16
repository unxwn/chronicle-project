from django.db import models


class NoteTag(models.Model):
    """Intermediate model for Note-Tag many-to-many relationship"""
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['note', 'tag']
        verbose_name = "Note Tag"
        verbose_name_plural = "Note Tags"

    def __str__(self):
        return f"{self.note.title} - {self.tag.name}"

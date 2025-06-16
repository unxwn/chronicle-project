from django.db import models


class ChecklistItem(models.Model):
    """Items for checklist notes (shopping lists, todo lists, etc.)"""
    note = models.ForeignKey(
        'Note',
        on_delete=models.CASCADE,
        related_name='checklist_items'
    )
    text = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)  # for ordering items
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Checklist Item"
        verbose_name_plural = "Checklist Items"

    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.text}"

    def save(self, *args, **kwargs):
        from django.utils import timezone
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)

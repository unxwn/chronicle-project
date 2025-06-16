from django.db import models
from django.conf import settings

class BoardMember(models.Model):
    """Intermediate model for Board-User many-to-one relationship"""
    BOARD_ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
        ('owner', 'Owner'),
    ]
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='board_memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='board_memberships')
    role = models.CharField(max_length=20, choices=BOARD_ROLE_CHOICES, default='viewer')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('board', 'user')

    def __str__(self):
        return f"{self.user.username} on {self.board.name} as {self.role}"

import random

from django.db import models
from django.conf import settings


def random_color():
    # відтінок між 0x444444 і 0xdddddd для помірної світлості
    return "#{:06x}".format(random.randint(0x444444, 0xdddddd))


class Board(models.Model):
    """Notes board"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BoardMember', related_name='boards')
    color = models.CharField(max_length=7, default='#007bff')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def text_color(self):
        hex = self.color.lstrip('#')
        r, g, b = tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
        # формула яскравості: (299*R + 587*G + 114*B)/1000
        lum = (299 * r + 587 * g + 114 * b) / 1000
        return 'black' if lum > 128 else 'white'

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"

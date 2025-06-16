import os
from django.db import models


def voice_note_path(instance, filename):
    """Generate upload path for voice notes"""
    return f'voice_notes/{instance.note.author.id}/{instance.note.id}/{filename}'


class VoiceNote(models.Model):
    """Voice recordings for voice-type notes"""
    note = models.OneToOneField(
        'Note',
        on_delete=models.CASCADE,
        related_name='voice_note'
    )
    audio_file = models.FileField(
        upload_to=voice_note_path,
        help_text="Supported formats: mp3, wav, ogg"
    )
    duration = models.PositiveIntegerField(
        help_text="Duration in seconds",
        null=True,
        blank=True
    )
    transcription = models.TextField(
        blank=True,
        help_text="Auto-generated or manual transcription"
    )
    file_size = models.PositiveIntegerField(help_text="Size in bytes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Voice Note"
        verbose_name_plural = "Voice Notes"

    def __str__(self):
        return f"Voice note for {self.note.title}"

    def save(self, *args, **kwargs):
        if self.audio_file:
            self.file_size = self.audio_file.size
        super().save(*args, **kwargs)

    @property
    def file_extension(self):
        if self.audio_file:
            return os.path.splitext(self.audio_file.name)[1].lower()
        return ""

    @property
    def duration_formatted(self):
        """Return duration in MM:SS format"""
        if self.duration:
            minutes = self.duration // 60
            seconds = self.duration % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"

    @property
    def file_size_formatted(self):
        """Return file size in human-readable format"""
        if self.file_size:
            if self.file_size < 1024:
                return f"{self.file_size} B"
            elif self.file_size < 1024 * 1024:
                return f"{self.file_size / 1024:.1f} KB"
            else:
                return f"{self.file_size / (1024 * 1024):.1f} MB"
        return "0 B"

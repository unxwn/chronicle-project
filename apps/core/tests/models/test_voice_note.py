from django.test import TestCase
from apps.core.models import User, Note, VoiceNote, Board
from django.core.files.uploadedfile import SimpleUploadedFile

class VoiceNoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='v', password='v')
        self.board = Board.objects.create(name='Family Board', owner=self.user)
        self.note = Note.objects.create(title='Note', author=self.user, board=self.board)

    def test_create_voice_note(self):
        audio = SimpleUploadedFile("voice.mp3", b"dummy audio data", content_type="audio/mpeg")
        vn = VoiceNote.objects.create(note=self.note, audio_file=audio, duration=42, file_size=15)
        self.assertEqual(vn.duration, 42)

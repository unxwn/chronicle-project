from django.test import TestCase
from apps.core.models import User, Note, Attachment, Board
from django.core.files.uploadedfile import SimpleUploadedFile

class AttachmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a', password='b')
        self.board = Board.objects.create(name='Family Board', owner=self.user)
        self.note = Note.objects.create(title='Note', author=self.user, board=self.board)

    def test_create_attachment(self):
        file = SimpleUploadedFile("doc.txt", b"test content", content_type="text/plain")
        attachment = Attachment.objects.create(
            note=self.note,
            file=file,
            original_filename='doc.txt',
            file_size=12
        )
        self.assertEqual(attachment.original_filename, 'doc.txt')

from django.test import TestCase
from apps.core.models import User, Note, Tag, Category, NoteTag, Board


class NoteTagModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a', password='b')
        self.board = Board.objects.create(name='Family Board', owner=self.user)
        self.note = Note.objects.create(title='Note', author=self.user, board=self.board)
        self.tag = Tag.objects.create(name='Tag')

    def test_create_note_tag(self):
        note_tag = NoteTag.objects.create(note=self.note, tag=self.tag)
        self.assertEqual(note_tag.note.title, 'Note')
        self.assertEqual(note_tag.tag.name, 'Tag')

from django.test import TestCase
from apps.core.models import User, Note, Category, Board, BoardMember


class NoteModelTest(TestCase):
    def setUp(self):
        """User and category creating before every test"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        self.board = Board.objects.create(name='Family Board', description="Test", owner=self.user)
        BoardMember.objects.create(board=self.board, user=self.user, role='owner')

        self.category = Category.objects.create(
            name='Work',
            description='Work related notes',
            color='#ffcc00'
        )

        self.note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
            'board': self.board,
            'note_type': 'text',
            'author': self.user,
            'category': self.category,
            'priority': 'medium',
            'is_pinned': False,
            'is_archived': False
        }

        self.note = Note.objects.create(**self.note_data)

    def test_create_note(self):
        """Check that the note is created correctly"""
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note_data['title'])
        self.assertEqual(note.content, self.note_data['content'])
        self.assertEqual(note.board.name, 'Family Board')
        self.assertEqual(note.note_type, 'text')
        self.assertEqual(note.author.username, 'testuser')
        self.assertEqual(note.category.name, 'Work')

    def test_update_note(self):
        """Update note fields"""
        self.note.title = 'Updated Title'
        self.note.priority = 'high'
        self.note.save()

        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.title, 'Updated Title')
        self.assertEqual(updated_note.priority, 'high')

    def test_delete_note(self):
        """Check that the note is deleted correctly"""
        note_id = self.note.id
        self.note.delete()

        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)

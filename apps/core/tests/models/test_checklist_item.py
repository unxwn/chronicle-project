from django.test import TestCase
from apps.core.models import User, Note, ChecklistItem, Board


class ChecklistItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a', password='b')
        self.board = Board.objects.create(name='Family Board', owner=self.user)
        self.note = Note.objects.create(title='Note', author=self.user, board=self.board)

    def test_create_checklist_item(self):
        item = ChecklistItem.objects.create(note=self.note, text='Buy milk', is_completed=True, order=1)
        self.assertEqual(item.text, 'Buy milk')
        self.assertTrue(item.is_completed)
        self.assertEqual(item.order, 1)

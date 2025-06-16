from django.test import TestCase
from apps.core.models import User, Note, TableData, Board


class TableDataModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a', password='b')
        self.board = Board.objects.create(name='Family Board', owner=self.user)
        self.note = Note.objects.create(title='Note', author=self.user, board=self.board)

    def test_create_table_data(self):
        table = TableData.objects.create(note=self.note, headers=["Name", "Age"], rows=[["Alice", "30"]])
        self.assertEqual(table.headers, ["Name", "Age"])
        self.assertEqual(table.rows, [["Alice", "30"]])

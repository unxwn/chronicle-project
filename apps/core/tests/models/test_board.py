from django.test import TestCase
from apps.core.models import User, Board, BoardMember

class BoardModelTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass')
    def test_create_board_and_membership(self):
        board = Board.objects.create(name='Family Board', owner=self.owner)
        member = BoardMember.objects.create(board=board, user=self.owner, role='owner')
        self.assertEqual(board.name, 'Family Board')
        self.assertEqual(board.owner, self.owner)
        self.assertTrue(board.members.filter(id=self.owner.id).exists())
        self.assertEqual(member.role, 'owner')

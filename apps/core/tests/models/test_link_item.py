from django.test import TestCase
from apps.core.models import User, Note, LinkItem, Board


class LinkItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.board = Board.objects.create(name='Family Board', owner=self.user)
        self.note = Note.objects.create(title='Note', author=self.user, board=self.board)

    def test_create_link_item(self):
        link = LinkItem.objects.create(
            note=self.note,
            title='Django',
            url='https://www.djangoproject.com/',
            description='Django site',
            order=1
        )
        self.assertEqual(link.title, 'Django')
        self.assertEqual(link.url, 'https://www.djangoproject.com/')

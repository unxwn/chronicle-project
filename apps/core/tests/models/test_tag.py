from django.test import TestCase
from apps.core.models import Tag

class TagModelTest(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name="Urgent")
        self.assertEqual(tag.name, "Urgent")

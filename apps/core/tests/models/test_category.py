from django.test import TestCase
from apps.core.models import Category

class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(
            name="Test Category",
            description="Test desc",
            color="#ffaa00"
        )
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test desc")
        self.assertEqual(category.color, "#ffaa00")

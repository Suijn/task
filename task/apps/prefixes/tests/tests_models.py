from django.test import TestCase

from task.apps.prefixes.models import Item, Prefix
from task.apps.prefixes.tests.factories import get_test_prefix


class TestPrefix(TestCase):
    def test_str(self):
        prefix = Prefix(name="dummy")
        self.assertEqual("dummy", str(prefix))


class TestItem(TestCase):
    def test_str(self):
        prefix = get_test_prefix()
        prefix.save()

        item = Item(name="dummy_item", prefix=prefix)
        self.assertEqual("dummy_item", str(item))

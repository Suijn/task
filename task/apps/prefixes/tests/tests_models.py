from django.test import TestCase

from task.apps.prefixes.models import Prefix


class TestPrefix(TestCase):
    def test_str(self):
        prefix = Prefix(name="dummy")
        self.assertEqual("dummy", str(prefix))

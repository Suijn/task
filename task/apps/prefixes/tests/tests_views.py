from django.test import TestCase
from rest_framework.test import APIClient

from task.apps.prefixes.models import Item, Prefix


class TestPrefixView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        prefix1 = Prefix.objects.create(name="prefix1")
        prefix2 = Prefix.objects.create(name="prefix2")
        prefix3 = Prefix.objects.create(name="prefix3")

        Item.objects.create(name="item1", prefix=prefix1)
        Item.objects.create(name="item2", prefix=prefix1)

        Item.objects.create(name="item3", prefix=prefix2)
        Item.objects.create(name="item4", prefix=prefix2)

        response = self.client.get("/api/prefixes/")
        self.assertEqual(200, response.status_code)

        expected_data = [
            {"name": "prefix1", "items": ["item1", "item2"], "pk": prefix1.pk},
            {"name": "prefix2", "items": ["item3", "item4"], "pk": prefix2.pk},
            {"name": "prefix3", "items": [], "pk": prefix3.pk},
        ]
        returned_data = response.json()
        self.assertEqual(expected_data, returned_data)

    def test_retrieve(self):
        prefix1 = Prefix.objects.create(name="prefix1")
        Prefix.objects.create(name="prefix2")

        Item.objects.create(name="item1", prefix=prefix1)
        Item.objects.create(name="item2", prefix=prefix1)

        response = self.client.get(f"/api/prefixes/{prefix1.pk}/")
        self.assertEqual(200, response.status_code)

        expected_data = {
            "name": "prefix1",
            "items": ["item1", "item2"],
            "pk": prefix1.pk,
        }
        returned_data = response.json()
        self.assertEqual(expected_data, returned_data)

    def test_retrieve__returns_404_if_not_found(self):
        response = self.client.get("/api/prefixes/prefix999/")
        self.assertEqual(404, response.status_code)

from django.test import TransactionTestCase
from rest_framework.test import APIClient

from task.apps.prefixes.models import Item, Prefix


class TestPrefixView(TransactionTestCase):
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
            {"name": "prefix1", "items": ["item1", "item2"], "id": prefix1.pk},
            {"name": "prefix2", "items": ["item3", "item4"], "id": prefix2.pk},
            {"name": "prefix3", "items": [], "id": prefix3.pk},
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
            "id": prefix1.pk,
        }
        returned_data = response.json()
        self.assertEqual(expected_data, returned_data)

    def test_retrieve__returns_404_if_not_found(self):
        response = self.client.get("/api/prefixes/prefix999/")
        self.assertEqual(404, response.status_code)

    def test_create(self):
        prefix = {"name": "prefix1"}
        response = self.client.post("/api/prefixes/", data=prefix)
        self.assertEqual(201, response.status_code)

        expected_response = {"name": "prefix1"}
        self.assertEqual(expected_response, response.json())

        prefix_created = Prefix.objects.get(name="prefix1")
        self.assertEqual("prefix1", prefix_created.name)
        self.assertEqual([], list(prefix_created.items.all()))

    def test_create__prefix_already_exists(self):
        existing_prefix1 = Prefix.objects.create(name="existing_prefix")
        Item.objects.create(name="item1", prefix=existing_prefix1)

        prefix = {"name": "existing_prefix"}
        response = self.client.post("/api/prefixes/", data=prefix)
        self.assertEqual(409, response.status_code)

        expected_response = {"conflict": "Prefix already exists."}
        self.assertEqual(expected_response, response.json())

        # Assert that the existing_prefix1 is still in the database and it still
        # has items that were assigned to it.
        prefix = Prefix.objects.get(name="existing_prefix")
        self.assertEqual("existing_prefix", prefix.name)

        expected_items = {("item1", "existing_prefix")}
        returned_items = {(item.name, item.prefix.name) for item in prefix.items.all()}
        self.assertEqual(expected_items, returned_items)

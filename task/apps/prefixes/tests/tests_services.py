from django.test import TestCase

from task.apps.prefixes.models import Item, Prefix, PrefixRaw
from task.apps.prefixes.services import map_items_to_prefixes


class TestMapItemsToPrefixes(TestCase):
    def test_map_items_to_prefixes(self):
        prefixes = [
            PrefixRaw(name="adhoc_charge_amt"),
            PrefixRaw(name="adhoc_charge_amt_usd"),
            PrefixRaw(name="admin_refund_amt"),
            PrefixRaw(name="alcohol_direct_payment_ind"),
            PrefixRaw(name="alcohol_tax_amt_usd"),
            PrefixRaw(name="alcohol_gmv_amt"),
            PrefixRaw(name="alcohol_gmv_amt_usd"),
            PrefixRaw(name="alcohol_product_ind"),
            PrefixRaw(name="arrived_customer_location_date_time_pt"),
            PrefixRaw(name="arrived_customer_location_date_time_utc"),
            PrefixRaw(name="bag"),
            PrefixRaw(name="bag_fee"),
            PrefixRaw(name="bag_fee_bar"),
            PrefixRaw(name="bag_fee_baz"),
            PrefixRaw(name="adhoc_charge_bar"),
        ]
        map_items_to_prefixes(prefixes, delimiter="_")

        expected_prefixes = {
            "adhoc_charge",
            "adhoc_charge_amt",
            "admin_refund",
            "alcohol_direct_payment",
            "alcohol_tax_amt",
            "alcohol_gmv",
            "alcohol_gmv_amt",
            "alcohol_product",
            "arrived_customer_location_date_time",
            "arrived_customer_location_date_time",
            "bag",
            "bag_fee",
        }
        prefixes_returned = set(prefix.name for prefix in Prefix.objects.all())
        self.assertEqual(expected_prefixes, prefixes_returned)

        expected_items = {
            ("amt", "adhoc_charge"),
            ("bar", "adhoc_charge"),
            ("usd", "adhoc_charge_amt"),
            ("amt", "admin_refund"),
            ("ind", "alcohol_direct_payment"),
            ("usd", "alcohol_tax_amt"),
            ("amt", "alcohol_gmv"),
            ("usd", "alcohol_gmv_amt"),
            ("ind", "alcohol_product"),
            ("pt", "arrived_customer_location_date_time"),
            ("utc", "arrived_customer_location_date_time"),
            ("fee", "bag"),
            ("bar", "bag_fee"),
            ("baz", "bag_fee"),
        }
        items = Item.objects.all().select_related("prefix")
        returned_items = set((item.name, item.prefix.name) for item in items)
        self.assertEqual(expected_items, returned_items)

    def test_map_items_to_prefixes__no_delimiter_in_raw_data(self):
        prefixes = [PrefixRaw("bag")]
        map_items_to_prefixes(prefixes, delimiter="_")

        prefixes_expected = {"bag"}
        prefixes_returned = set(prefix.name for prefix in Prefix.objects.all())

        self.assertEqual(prefixes_expected, prefixes_returned)

    def test_map_items_to_prefixes__prefix_can_store_multiple_items(self):
        prefixes = [PrefixRaw("foo_bar"), PrefixRaw("foo_baz")]
        map_items_to_prefixes(prefixes, delimiter="_")

        prefixes_expected = {"foo"}
        prefixes_returned = set(prefix.name for prefix in Prefix.objects.all())

        self.assertEqual(prefixes_expected, prefixes_returned)

        items_expected = {("bar", "foo"), ("baz", "foo")}
        items = Item.objects.all().select_related("prefix")
        items_returned = set((item.name, item.prefix.name) for item in items)
        self.assertEqual(items_expected, items_returned)

    def test_map_items_to_prefixes__handles_different_delimiter(self):
        prefixes = [PrefixRaw("prefix1.item1"), PrefixRaw("prefix2.item2")]
        map_items_to_prefixes(prefixes, delimiter=".")

        expected_prefixes = {"prefix1", "prefix2"}
        returned_prefixes = {prefix.name for prefix in Prefix.objects.all()}
        self.assertEqual(expected_prefixes, returned_prefixes)

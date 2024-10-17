import structlog
from django.core.exceptions import ObjectDoesNotExist

from task.apps.prefixes.models import Item, Prefix, PrefixRaw

logger = structlog.get_logger()


def map_items_to_prefixes(prefixes: list[PrefixRaw], delimiter: str = "_"):
    """
    Based on the list of PrefixRaw objects,
    map Items to Prefixes and put it to the database.

    For:
    prefixes = [
        PrefixRaw(name="adhoc_charge_amt"),
        PrefixRaw(name="adhoc_charge_amt_usd"),
        PrefixRaw(name="admin_refund_amt")
    ]

    this function will extract the following prefixes:
        prefix1 = Prefix(name="adhoc_charge")
        prefix2 = Prefix(name="adhoc_charge_amt")
        prefix3 = Prefix(name="admin_refund")

    and items:
        item1 = Item(name="amt", prefix=prefix1)
        item2 = Item(name="usd", prefix=prefix2)
        item3 = Item(name="amt", prefix=prefix3)

    The results will be stored in the database.
    """

    for raw_prefix in prefixes:
        log = logger.bind(raw_prefix=raw_prefix)

        prefix = raw_prefix.name.split(delimiter)[:-1]
        prefix = "_".join(prefix)

        if prefix:
            item = raw_prefix.name.split("_")[-1]

            try:
                existing = Prefix.objects.get(name=prefix)
            except ObjectDoesNotExist:
                _prefix = Prefix.objects.create(name=prefix)
                Item.objects.create(name=item, prefix=_prefix)

                log.info("Created new prefix", prefix=prefix, item=item)
            else:
                Item.objects.create(name=item, prefix=existing)

                log.info(
                    "Prefix already exists, appending item", prefix=prefix, item=item
                )

        # if prefix is not found after splitting
        # then treat the last element as a prefix without any item.
        # example: raw input: "source"
        else:
            prefix = raw_prefix.name.split("_")[-1]

            try:
                existing = Prefix.objects.get(name=prefix)
            except ObjectDoesNotExist:
                _prefix = Prefix.objects.create(name=prefix)
                log.info("Created new prefix", prefix=prefix)
            else:
                log.info("Prefix already exists, skipping", prefix=prefix)
                continue

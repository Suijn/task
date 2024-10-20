from task.apps.prefixes.models import Prefix


def get_test_prefix(name: str = "dummy") -> Prefix:
    return Prefix(name=name)

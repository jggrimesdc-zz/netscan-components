"""
Uses a column definition to determine an appropriate fake data type
"""
import datetime as dt
import random
import re
from data_gen import settings
from data_gen.generate import Rule
from data_gen.keyspace import Column
from faker import Faker, providers
from typing import Iterable, Any, List, Optional

fake = Faker()
fake.add_provider(providers.internet)
fake.add_provider(providers.company)
fake.add_provider(providers.date_time)

NAME_RULES: List[Rule] = Rule.get_list_from_file(settings.RULES_FILE)


def how_many() -> Iterable:
    """ Returns a `range` iterator for random count between `settings.MIN_LIST_ITEMS` and `settings.MAX_LIST_ITEMS` """
    count = random.randint(settings.MIN_LIST_ITEMS, settings.MAX_LIST_ITEMS)
    return range(count)


def when() -> dt.datetime:
    """ Returns a timestamp for a random datetime between `settings.MIN_DATETIME` and `settings.MAX_DATETIME` """
    return fake.date_time_between(
        start_date=settings.MIN_DATETIME, end_date=settings.MAX_DATETIME
    ).isoformat()


def fake_column_data(column: Column, extra_rules: Optional[List[Rule]] = None):
    if column.type in ("list", "set"):
        return [
            get_data_for_column(column, extra_rules=extra_rules) for _ in how_many()
        ]
    elif column.type in ("map", "dict", "mapping"):
        return dict(
            (fake.name(), get_data_for_column(column, extra_rules=extra_rules))
            for _ in how_many()
        )
    return get_data_for_column(column, extra_rules=extra_rules)


def get_data_for_column(
        column: Column, extra_rules: Optional[List[Rule]] = None
) -> Any:
    data = get_data_for_name(column.name, extra_rules=extra_rules)
    if data is not None:
        return data
    return get_data_for_type(column.type)


def get_data_for_type(t: str) -> Any:
    if t == "text":
        return fake.word()
    elif t in ("numeric", "int"):
        return fake.random_number(digits=18)
    elif t in ("datetime", "timestamp"):
        return when()
    elif t == "float":
        return fake.random_number(digits=18) * random.random()
    return None


def get_data_for_name(name: str, extra_rules: Optional[List[Rule]] = None) -> Any:
    rules = NAME_RULES
    if extra_rules:
        rules = extra_rules + rules
    for rule in rules:
        result = rule.run(name)
        if result is not None:
            return result
    return None

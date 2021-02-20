import json
import re
from data_gen import settings
from data_gen.keyspace import Column
from faker import Faker, providers

fake = Faker()
fake.add_provider(providers.internet)
fake.add_provider(providers.company)
fake.add_provider(providers.date_time)


class Rule(object):
    """ A data loading rule """

    def __init__(self, pattern: str, method: str, extra_args: dict):
        self.pattern = re.compile(pattern.replace(r"\b", r"(\b|_)"), re.IGNORECASE)
        self.method = getattr(fake, method)
        self.extra_args = extra_args

    def run(self, name: str):
        """ True if `self.pattern` found in `name` """
        if self.pattern.search(name):
            return self.method(**self.extra_args)
        return None

    @classmethod
    def from_list(cls, l: list):
        extra_args = l[2] if len(l) > 2 else {}
        return cls(l[0], l[1], extra_args)

    @classmethod
    def get_list_from_file(cls, path: str):
        with open(path) as f:
            data = json.loads(f.read())
        return [cls.from_list(rule) for rule in data["rules"]]

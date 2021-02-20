""" A column representation """


class Column(object):
    __doc__ = __doc__

    def __init__(self, definition: str):
        parts = definition.split(" ")

        if len(parts) != 2:
            raise TypeError(f'Definition "{definition}" is improperly formatted!')

        self.name = parts[0]
        self.type = parts[1]

    @property
    def definition(self) -> str:
        return f"{self.name} {self.type}"

    def __str__(self):
        return self.definition

    def __repr__(self):
        return f'Column("{self.definition}")'

    def __eq__(self, other):
        if not isinstance(other, Column):
            return False
        return self.name == other.name and self.type == other.type

    def __hash__(self):
        return hash(repr(self))

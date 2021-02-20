import pytest

from data_gen.generate import fake_column
from data_gen.keyspace import Column

with open("data/test_conf/cols.txt") as f:
    col_data = [Column(x) for x in f.read().split("\n") if x]


@pytest.fixture
def cols():
    return col_data


@pytest.fixture(params=col_data)
def col(request):
    return request.param


def test_columns_hit(col):
    """ make sure each column has a match """
    data = fake_column.fake_column_data(col)
    # res = f'name: {col.name}, type: {col.type}, data: {data}'
    assert data is not None

# def test_counts(cols):
#     """ get a count of how many matches work by each type """
#     missing = []
#     for col in cols:
#         hit = fake_column.get_data_for_name(col.name)
#         if col.type == 'text' and hit is None:
#             missing.append(col)

#     cnt = len(missing)

#     assert len(missing) < len(cols) // 2

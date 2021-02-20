import json
import pytest
from data_gen.generate.fake import fake_column_data, fake_data
from data_gen.keyspace import KeyspaceReader
from pathlib import Path


@pytest.mark.parametrize('override_file', [Path('data/test_conf/override_data.ndjson'), None])
def test_fake_data(override_file: Path, manager):
    output_dir = Path('tmp/test/fake_data')
    if override_file:
        output_dir /= f"{manager.name}_{override_file.name.replace(override_file.suffix, '')}"
    else:
        output_dir /= manager.name
    fake_data(manager, output_dir, override_file=override_file)

    for path in output_dir.glob('**/*.ndjson'):
        with open(str(path)) as f:
            assert len(f.read()) > 0

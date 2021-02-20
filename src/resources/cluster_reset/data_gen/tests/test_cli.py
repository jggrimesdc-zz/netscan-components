import pytest

from data_gen import cli


@pytest.mark.parametrize(
    "input_command,expected",
    [
        (
                "generate --n_rows 10 foo bar".split(" "),
                {"n_rows": 10, "generate": True, "upload": False},
        ),
        (
                "generate --upload foo bar".split(" "),
                {"upload": True, "generate": True},
        ),
        (
                'generate --override_file baz foo bar'.split(' '),
                {'override_file': 'baz'}
        ),
        (
                'upload foo bar'.split(' '),
                {'upload': True, 'generate': False}
        )
    ],
)
def test_cli_parser(input_command, expected):
    args = cli.parse_args(input_command)
    observerd = vars(args)

    for key, val in expected.items():
        assert observerd[key] == val

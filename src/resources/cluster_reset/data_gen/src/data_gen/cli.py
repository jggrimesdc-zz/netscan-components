import argparse
from data_gen.generate.fake import fake_data
from data_gen.keyspace import KeyspaceReader
from data_gen.load import load_data
from pathlib import Path
from typing import Optional


def parse_args(args: Optional[list] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyspace_pattern", "-p", type=str, default="**/*.json")
    parser.set_defaults(generate=False, upload=True)

    subparsers = parser.add_subparsers(help="sub-commands")

    generate_parser = subparsers.add_parser("generate", help="Generate a new dataset")
    generate_parser.set_defaults(generate=True)
    generate_parser.add_argument(
        "--n_rows", type=int, help="number of rows to generate", default=5
    )
    generate_parser.add_argument(
        "--upload", action="store_true", help="upload the newly generated data"
    )
    generate_parser.add_argument(
        "--override_file",
        type=str,
        help="path to file containing data that will override generated values",
    )

    load_parser = subparsers.add_parser("upload", help="upload an existing dataset")
    load_parser.set_defaults(upload=True)

    parser.add_argument("keyspace_path", type=str, help="path to a keyspace folder")
    parser.add_argument(
        "data_dir", type=str, help="destination to output data to or source data from"
    )
    return parser.parse_args(args)


def handle(event, context):
    args = parse_args()

    reader = KeyspaceReader(args.keyspace_path, args.keyspace_pattern)
    manager = reader.read()

    if args.generate:
        fake_data(
            manager,
            Path(args.data_dir),
            n_rows=args.n_rows,
            override_file=Path(args.override_file) if args.override_file else None,
        )

    if args.upload:
        load_data(manager, Path(args.data_dir))


if __name__ == "__main__":
    handle()

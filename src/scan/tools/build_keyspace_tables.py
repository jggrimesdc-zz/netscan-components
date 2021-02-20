""" Methods to rebuild all tables defined within a keyspace """

import argparse
import json
import requests

from scan import settings
from scan.logger import logger
from scan.tools.defaulter import default_kwargs_from_settings


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyspace", type=str, help="Keyspace to build table(s) in.")
    parser.add_argument("--url", type=str, help="URL to base API to build table(s) in.")
    parser.add_argument(
        "--cluster_id", type=str, help="Cluster ID to build table(s) in."
    )
    parser.add_argument(
        "--account_id",
        type=str,
        help="Account ID. Defaults to ACCOUNT_ID in settings.py.",
    )
    parser.add_argument(
        "--user_id", type=str, help="User ID. Defaults to USER_ID in settings.py."
    )
    return parser.parse_args()


@default_kwargs_from_settings("account_id", "user_id")
def build_keyspace_tables(
        keyspace: str, url: str, account_id: str = None, user_id: str = None
):
    """ Build tables in keyspace ``keyspace`` """
    logger.info('Building tables in keyspace "%s".', keyspace)
    tables = get_keyspace_table_names_and_configs(keyspace)
    for table_name, table_definition in tables:
        build_keyspace_table(
            url, keyspace, table_name, table_definition, account_id, user_id
        )
    logger.info('Built tables for keyspace "%s".', keyspace)


def handle(event, context):
    """ CLI entrypoint """
    args = get_args()

    build_keyspace_tables(
        keyspace=args.keyspace,
        url=args.url,
        account_id=args.account_id,
        user_id=args.user_id,
    )


def get_keyspace_table_names_and_configs(keyspace):
    """ Fetch all configs for files in a given keyspace """
    keyspace_path = settings.RESOURCE_PATH / "cluster_reset" / "config" / keyspace
    return [
        (table_config.with_suffix("").parts[-1], json.loads(table_config.read_text()),)
        for table_config in keyspace_path.glob("*.json")
    ]


@default_kwargs_from_settings("account_id", "user_id")
def build_keyspace_table(
        keyspace: str,
        url: str,
        table_name: str,
        table_definition: dict,
        account_id: str = None,
        user_id: str = None,
):
    """ Build a table from JSON config in a keyspace """
    headers = {
        "accept": "*/*",
        "X-netscan-CustomerAccountId": account_id,
        "X-netscan-UserId": user_id,
    }

    logger.info('Removing existing table "%s".', table_name)
    requests.delete(f"{url}/{table_name}", headers=headers)
    logger.info('Removed table "%s".', table_name)

    logger.info('Creating table "%s".', table_name)
    headers["Content-Type"] = "application/json"
    data = table_definition
    requests.post(url, headers=headers, data=data)
    logger.info('Created table "%s".', table_name)


if __name__ == "__main__":
    handle()

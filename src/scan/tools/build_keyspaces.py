import argparse
import requests
from typing import List

from scan import settings
from scan.logger import logger
from scan.tools.defaulter import default_kwargs_from_settings


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "keyspaces",
        type=str,
        help='Keyspaces to build, separated by comma (e.g. "foo,bar"). To build all keyspaces in ``settings``, use "*"',
    )
    parser.add_argument(
        "--account_id",
        type=str,
        help="ID of account to build keyspaces as. Defaults to ``settings.ACCOUNT_ID``.",
    )
    parser.add_argument(
        "--user_id",
        type=str,
        help="ID of user to build keyspaces as. Defaults to ``settings.USER_ID``.",
    )
    parser.add_argument(
        "--cluster_id",
        type=str,
        help="ID of cluster to build keyspaces in. Defaults to ``settings.CLUSTER_ID``.",
    )
    parser.add_argument(
        "--no_build_tables",
        action="store_false",
        help="After building keyspace, do not build tables",
    )
    return parser.parse_args()


def handle(event, context):
    args = get_args()
    if args.keyspaces == "*":
        keyspaces = settings.KEYSPACES
    else:
        keyspaces = args.keyspaces.split(",")

    url = settings.BASE_URL + settings.CLUSTER_ENDPOINT

    build_keyspaces(
        keyspaces,
        url=url,
        account_id=args.account_id,
        user_id=args.user_id,
        cluster_id=args.cluster_id,
    )


@default_kwargs_from_settings("account_id", "user_id", "cluster_id")
def build_keyspaces(
        keyspaces: list = None,
        url: str = None,
        account_id: str = None,
        user_id: str = None,
        cluster_id: str = None,
):
    """ Builds a set of keyspaces """
    logger.info("Building keyspaces: %s", keyspaces)
    for keyspace in keyspaces:
        build_keyspace(keyspace, account_id, user_id, cluster_id, url)
    logger.info("Successfully built keyspaces.")


@default_kwargs_from_settings("account_id", "user_id", "cluster_id")
def build_keyspace(
        keyspace: str,
        account_id: str = None,
        user_id: str = None,
        cluster_id: str = None,
        url: str = None,
):
    """ Builds a single keyspace """
    logger.info('Building keyspace "%s"...')
    headers = {
        "X-netscan-CustomerAccountId": account_id,
        "X-netscan-UserId": user_id,
        "accept": "*/*",
    }

    logger.info('Removing existing keyspace "%s"...')
    requests.delete(f"{url}/keyspaces/{keyspace}", headers=headers)
    logger.info('Keyspace "%s" has been deleted!')

    logger.info('Creating keyspace "%s"...')
    headers["Content-Type"] = "application/json"
    data = {
        "name": keyspace,
        "replicationFactorMainDatacenter": settings.REPLICATION_FACTOR_MAIN_DATACENTER,
        "replicationFactorSecondDatacenter": settings.REPLICATION_FACTOR_SECOND_DATACENTER,
    }
    requests.post(f"{url}/keyspaces", headers=headers, data=data)
    logger.info('Keyspace "%s" has been created!')

    logger.info('Ensuring filtering allowed on cluster.')
    data = {"allowFiltering": True}
    requests.put(f"{url}/filter", headers=headers, data=data)

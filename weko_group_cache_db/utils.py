#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Utils module for weko-group-cache-db."""

import traceback
import typing as t

from datetime import UTC, datetime
from urllib.parse import urljoin

import redis
import requests

from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

from .config import config
from .loader import Institution, load_institutions
from .logger import console, logger
from .redis import connection

if t.TYPE_CHECKING:
    from redis import Redis


def fetch_all(file_path: str) -> int:
    """Fetch and cache groups for all institutions.

    Arguments:
        file_path (str): Path to the TOML file containing institution data.

    Returns:
        int: Exit code (0 for success, 1 for failure).

    """
    store = connection()
    institutions = load_institutions(file_path)
    code = 0

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            "Fetching and caching groups for all institutions", total=len(institutions)
        )

        for institution in institutions:
            try:
                group_ids = fetch_map_groups(institution)
                set_groups_to_redis(institution.fqdn, group_ids, store=store)

                progress.log(f"{len(group_ids)} groups cached for {institution.fqdn}.")
            except requests.RequestException:
                traceback.print_exc()
                code = 1
            except redis.RedisError:
                logger.error(
                    "Failed to cache groups to Redis for institution: %s",
                    institution.fqdn,
                )
                traceback.print_exc()
                code = 1
            finally:
                progress.update(task, advance=1)

    return code


def fetch_one(file_path: str, fqdn: str):
    """Fetch and cache groups for a specific institution.

    Arguments:
        file_path (Path): Path to the TOML file containing institution data.
        fqdn (str): FQDN of the target institution.

    Raises:
        RequestException: If the HTTP request fails.
        RedisError: If caching to Redis fails.

    """
    store = connection()
    institutions = load_institutions(file_path)

    target_institution = next(
        (inst for inst in institutions if inst.fqdn == fqdn), None
    )

    if target_institution is None:
        logger.error("Institution with FQDN %s not found.", fqdn)
        return

    with console.status(f"Fetching and caching groups for institution: {fqdn}"):
        try:
            group_ids = fetch_map_groups(target_institution)
            set_groups_to_redis(target_institution.fqdn, group_ids, store=store)
        except requests.RequestException:
            raise
        except redis.RedisError:
            logger.error("Failed to cache groups to Redis for institution: %s", fqdn)
            raise
        else:
            logger.info("Successfully cached %d groups for %s.", len(group_ids), fqdn)


def fetch_map_groups(institution: Institution) -> list[str]:
    """Fetch and cache groups for the given institution.

    Arguments:
        institution (Institution): Institution object.

    Returns:
        list[str]: List of group IDs.

    Raises:
        RequestException: If the HTTP request fails.

    """
    fqdn = institution.fqdn

    endpoint = urljoin(config.MAP_GROUPS_API_ENDPOINT, institution.sp_connector_id)
    try:
        response = requests.get(
            endpoint,
            cert=(institution.client_cert_path, institution.client_key_path),
            timeout=config.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        group_entries = response.json().get("entry", [])
    except requests.RequestException:
        logger.error(
            "Failed to fetch groups from Gakunin API for institution: %s", fqdn
        )
        raise

    group_ids: list[str] = [
        group["id"].split("/")[-1] for group in group_entries if "id" in group
    ]

    return group_ids


def set_groups_to_redis(fqdn: str, group_ids: list[str], *, store: Redis | None = None):
    """Set groups to redis.

    Arguments:
        fqdn(str): fqdn of the target sp
        group_ids(list[str]): list of group ids
        store(Redis | None):
            Redis store object. If None, a new connection will be established.

    """
    transformed_fqdn = fqdn.replace(".", "_").replace("-", "_")
    redis_key = transformed_fqdn + config.CACHE_KEY_SUFFIX
    updated_at = datetime.now(UTC).isoformat(timespec="seconds")

    if store is None:
        store = connection()

    store.hset(
        redis_key, mapping={"updated_at": updated_at, "groups": ",".join(group_ids)}
    )
    store.persist(redis_key)
    if config.CACHE_TTL >= 0:
        store.expire(redis_key, config.CACHE_TTL)

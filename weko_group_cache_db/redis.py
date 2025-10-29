#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Redis connection module for weko-group-cache-db."""

import rich_click as click

from redis import Redis, sentinel

from .config import config


def connection() -> Redis:
    """Establish Redis connection.

    Returns:
        Redis: Redis store object.

    Raises:
        ValueError: If configuration for Redis is invalid.
        ConnectionError: If failed to connect to Redis.

    """
    try:
        if config.REDIS_TYPE == "redis":
            return _redis_connection()

        return _sentinel_connection()
    except ValueError:
        click.echo("Failed to connect to Redis. Invalid configuration.")
        raise
    except ConnectionError:
        click.echo("Failed to connect to Redis. Something went wrong on Redis.")
        raise


def _redis_connection() -> Redis:
    """Establish Redis connection and return Redis store object.

    Returns:
    Redis: Redis store object.

    """
    redis_url = config.REDIS_URL
    return Redis.from_url(redis_url)


def _sentinel_connection() -> Redis:
    """Establish Redis sentinel connection.

    Returns:
        Redis: Redis store object

    """
    sentinels = sentinel.Sentinel(config.REDIS_SENTINELS, decode_responses=False)
    return sentinels.master_for(config.REDIS_SENTINEL_MASTER, db=config.REDIS_DB_INDEX)

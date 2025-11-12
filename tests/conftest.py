#
# Copyright (C) 2025 National Institute of Informatics.
#

import typing as t

from logging import INFO

import pytest

from click.testing import CliRunner

from weko_group_cache_db.config import Settings, _current_config


@pytest.fixture
def runner(monkeypatch):
    """Fixture for invoking command-line interfaces.

    Returns:
        CliRunner: A CliRunner instance.

    """
    monkeypatch.setenv("COLUMNS", "80")
    return CliRunner()


@pytest.fixture
def set_test_config():
    def _set_test_config(**kwargs: t.Any) -> None:
        kwargs.setdefault("MAP_GROUPS_API_ENDPOINT", "https://sample.gakunin.jp/api/groups/")
        test_config = Settings(**kwargs)
        _current_config.set(test_config)

    return _set_test_config


@pytest.fixture
def row_config():
    return {
        "DEVELOPMENT": True,
        "LOG_LEVEL": "WARNING",
        "SP_CONNECTOR_ID_PREFIX": "test_jc_",
        "CACHE_KEY_SUFFIX": "_test_gakunin_groups",
        "CACHE_TTL": 43200,
        "MAP_GROUPS_API_ENDPOINT": "https://sample.gakunin.jp/api/groups/",
        "REQUEST_TIMEOUT": 25,
        "REQUEST_INTERVAL": 10,
        "REQUEST_RETRIES": 5,
        "REDIS_TYPE": "sentinel",
        "REDIS_HOST": "redis",
        "REDIS_PORT": 26379,
        "REDIS_DB_INDEX": 2,
        "REDIS_SENTINEL_MASTER": "testmaster",
        "SENTINELS": [{"host": "redis1", "port": 26378}, {"host": "redis2", "port": 26377}],
    }


@pytest.fixture
def log_capture(caplog) -> pytest.LogCaptureFixture:
    """Fixture for capturing logs.

    Args:
        caplog (LogCaptureFixture): A LogCaptureFixture instance.

    Returns:
        LogCaptureFixture: A LogCaptureFixture instance.

    """
    caplog.set_level(INFO)
    return caplog

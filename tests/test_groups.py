#
# Copyright (C) 2025 National Institute of Informatics.
#

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest
import redis
import requests

from weko_group_cache_db.exc import UpdateError
from weko_group_cache_db.groups import fetch_all, fetch_and_cache, fetch_map_groups, fetch_one, set_groups_to_redis
from weko_group_cache_db.loader import Institution


def test_fetch_all_success_toml(institutions_data, set_test_config, log_capture):
    num_institutions = 2
    data = institutions_data(num_institutions)
    institutions = [Institution(**data[0]), Institution(**data[1])]
    set_test_config()

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions") as mock_load,
        patch("weko_group_cache_db.groups.fetch_and_cache") as mock_fetch_and_cache,
        patch("weko_group_cache_db.groups.time") as mock_time,
    ):
        mock_load.return_value = institutions
        mock_func = MagicMock(side_effect=[2, 3])
        mock_fetch_and_cache.return_value = mock_func

        fetch_all(toml_path="institutions.toml")

    mock_load.assert_called_once_with(toml_path="institutions.toml")
    assert mock_func.call_count == num_institutions
    assert mock_func.call_args_list[0][0] == (institutions[0], mock_store)
    assert mock_func.call_args_list[1][0] == (institutions[1], mock_store)
    assert log_capture.records[0].getMessage() == f"Successfully cached 2 groups for {data[0]['fqdn']}."
    assert log_capture.records[1].getMessage() == f"Successfully cached 3 groups for {data[1]['fqdn']}."
    mock_time.sleep.assert_called_once()


def test_fetch_all_success_directory(institutions_data, set_test_config, log_capture):
    num_institutions = 2
    data = institutions_data(num_institutions)
    institutions = [Institution(**data[0]), Institution(**data[1])]
    set_test_config()

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions") as mock_load,
        patch("weko_group_cache_db.groups.fetch_and_cache") as mock_fetch_and_cache,
        patch("weko_group_cache_db.groups.time") as mock_time,
    ):
        mock_load.return_value = institutions
        mock_func = MagicMock(side_effect=[2, 3])
        mock_fetch_and_cache.return_value = mock_func

        fetch_all(directory_path="institutions", fqdn_list_file="fqdn_list.txt")

    mock_load.assert_called_once_with(directory_path="institutions", fqdn_list_file="fqdn_list.txt")
    assert mock_func.call_count == num_institutions
    assert mock_func.call_args_list[0][0] == (institutions[0], mock_store)
    assert mock_func.call_args_list[1][0] == (institutions[1], mock_store)
    assert log_capture.records[0].getMessage() == f"Successfully cached 2 groups for {data[0]['fqdn']}."
    assert log_capture.records[1].getMessage() == f"Successfully cached 3 groups for {data[1]['fqdn']}."
    mock_time.sleep.assert_called_once()


def test_fetch_all_no_institutions(set_test_config, log_capture):
    set_test_config()
    with (
        patch("weko_group_cache_db.groups.connection"),
        patch("weko_group_cache_db.groups.load_institutions", return_value=[]),
        patch("weko_group_cache_db.groups.time"),
    ):
        fetch_all(toml_path="empty_institutions.toml")
        assert log_capture.records[0].getMessage() == "No institutions found to fetch and cache groups for."


def test_fetch_all_request_error(institutions_data, set_test_config, log_capture):
    data = institutions_data(2)
    institutions = [Institution(**data[0]), Institution(**data[1])]

    test_config = set_test_config()
    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions", return_value=institutions),
        patch("weko_group_cache_db.groups.fetch_and_cache") as mock_fetch_and_cache,
        patch("weko_group_cache_db.groups.time"),
    ):
        num_groups = 2
        mock_func = MagicMock(side_effect=[num_groups, requests.RequestException("Request failed")])
        mock_fetch_and_cache.return_value = mock_func

        with pytest.raises(ExceptionGroup, match=r"Failed to update information from [1-9]+ institution\(s\)\.") as eg:
            fetch_all(toml_path="institutions.toml")

    assert mock_func.call_args_list[0][0] == (institutions[0], mock_store)
    assert mock_func.call_args_list[1][0] == (institutions[1], mock_store)
    assert log_capture.records[0].getMessage() == f"Successfully cached {num_groups} groups for {data[0]['fqdn']}."
    assert log_capture.records[1].getMessage() == (
        f"Despite retries {test_config.REQUEST_RETRIES} times, failed to cache groups "
        f"to Redis for institution: {data[1]['fqdn']}."
    )
    error_instance = eg.value.exceptions[0]
    assert isinstance(error_instance, UpdateError)
    assert isinstance(error_instance.origin, requests.RequestException)
    assert str(error_instance) == f"FQDN: {data[1]['fqdn']}, Request failed"


def test_fetch_all_redis_error(institutions_data, set_test_config, log_capture):
    data = institutions_data(1)
    institutions = [Institution(**data[0])]
    test_config = set_test_config()

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions", return_value=institutions),
        patch("weko_group_cache_db.groups.fetch_and_cache") as mock_fetch_and_cache,
        patch("weko_group_cache_db.groups.time"),
    ):
        mock_func = MagicMock(side_effect=redis.RedisError("Cache error"))
        mock_fetch_and_cache.return_value = mock_func

        with pytest.raises(ExceptionGroup, match=r"Failed to update information from [1-9]+ institution\(s\)\.") as eg:
            fetch_all(toml_path="institutions.toml")

    assert mock_func.call_args_list[0][0] == (institutions[0], mock_store)
    assert log_capture.records[0].getMessage() == (
        f"Despite retries {test_config.REQUEST_RETRIES} times, failed to cache groups "
        f"to Redis for institution: {data[0]['fqdn']}."
    )
    error_instance = eg.value.exceptions[0]
    assert isinstance(error_instance, UpdateError)
    assert isinstance(error_instance.origin, redis.RedisError)
    assert str(error_instance) == f"FQDN: {data[0]['fqdn']}, Cache error"


def test_fetch_one_success_toml(institutions_data, set_test_config, log_capture):
    data = institutions_data(2)
    institutions = [Institution(**data[0]), Institution(**data[1])]
    set_test_config()

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions") as mock_load,
        patch("weko_group_cache_db.groups.fetch_and_cache") as mock_fetch_and_cache,
    ):
        mock_load.return_value = institutions
        num_groups = 2
        mock_func = MagicMock(return_value=num_groups)
        mock_fetch_and_cache.return_value = mock_func

        fetch_one(institutions[0].fqdn, toml_path="institutions.toml")

    mock_load.assert_called_once_with(toml_path="institutions.toml")
    mock_func.assert_called_once_with(institutions[0], mock_store)
    assert log_capture.records[0].getMessage() == f"Successfully cached {num_groups} groups for {data[0]['fqdn']}."


def test_fetch_one_success_directory(institutions_data, set_test_config, log_capture):
    data = institutions_data(2)
    institutions = [Institution(**data[0]), Institution(**data[1])]
    set_test_config()

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions") as mock_load,
        patch("weko_group_cache_db.groups.fetch_and_cache") as mock_fetch_and_cache,
    ):
        mock_load.return_value = institutions
        num_groups = 3
        mock_func = MagicMock(return_value=num_groups)
        mock_fetch_and_cache.return_value = mock_func

        fetch_one(institutions[1].fqdn, directory_path="institutions", fqdn_list_file="fqdn_list.txt")

    mock_load.assert_called_once_with(directory_path="institutions", fqdn_list_file="fqdn_list.txt")
    mock_func.assert_called_once_with(institutions[1], mock_store)
    assert log_capture.records[0].getMessage() == f"Successfully cached {num_groups} groups for {data[1]['fqdn']}."


def test_fetch_one_institution_not_found(set_test_config, log_capture):
    set_test_config()
    mock_store = MagicMock()
    fqdn = "notfound.example.com"
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions", return_value=[]),
        pytest.raises(ValueError, match=r"Institution with FQDN [\w\.]+ not found."),
    ):
        fetch_one(fqdn, toml_path="institutions.toml")
    assert log_capture.records[0].getMessage() == f"Institution with FQDN {fqdn} not found."


def test_fetch_one_request_error(institutions_data, set_test_config, log_capture):
    data = institutions_data(1)
    institutions = [Institution(**data[0])]
    set_test_config()

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions", return_value=institutions),
        patch("weko_group_cache_db.groups.fetch_and_cache") as mock_fetch_and_cache,
    ):
        mock_func = MagicMock(side_effect=requests.RequestException("Request failed"))
        mock_fetch_and_cache.return_value = mock_func

        with pytest.raises(UpdateError, match=r"Request failed"):
            fetch_one(institutions[0].fqdn, toml_path="institutions.toml")

    mock_func.assert_called_once_with(institutions[0], mock_store)
    assert log_capture.records[0].getMessage() == (
        f"Despite retries {set_test_config().REQUEST_RETRIES} times, failed to cache groups to Redis "
        f"for institution: {data[0]['fqdn']}."
    )


def test_fetch_one_redis_error(institutions_data, set_test_config, log_capture):
    data = institutions_data(1)
    institutions = [Institution(**data[0])]
    set_test_config()

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store),
        patch("weko_group_cache_db.groups.load_institutions", return_value=institutions),
        patch("weko_group_cache_db.groups.fetch_and_cache") as mock_fetch_and_cache,
    ):
        mock_func = MagicMock(side_effect=redis.RedisError("Cache error"))
        mock_fetch_and_cache.return_value = mock_func

        with pytest.raises(UpdateError, match=r"Cache error"):
            fetch_one(institutions[0].fqdn, toml_path="institutions.toml")

    mock_func.assert_called_once_with(institutions[0], mock_store)
    assert log_capture.records[0].getMessage() == (
        f"Despite retries {set_test_config().REQUEST_RETRIES} times, failed to cache groups to Redis "
        f"for institution: {data[0]['fqdn']}."
    )


def test_fetch_and_cache_success(institutions_data, set_test_config):
    data = institutions_data(1)
    institution = Institution(**data[0])
    set_test_config()
    groups = ["jc_group1", "jc_group2"]

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.fetch_map_groups") as mock_fetch,
        patch("weko_group_cache_db.groups.set_groups_to_redis") as mock_set,
    ):
        mock_fetch.return_value = groups

        func = fetch_and_cache()
        count = func(institution, mock_store)

    assert count == len(groups)
    mock_fetch.assert_called_once_with(institution)
    mock_set.assert_called_once_with(institution.fqdn, groups, store=mock_store)


def test_fetch_and_cache_all_request_exception(institutions_data, set_test_config, log_capture):
    data = institutions_data(1)
    institution = Institution(**data[0])
    test_config = set_test_config(REQUEST_RETRY_FACTOR=0, REQUEST_RETRIES=2)

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.fetch_map_groups") as mock_fetch,
        patch("weko_group_cache_db.groups.set_groups_to_redis") as mock_set,
    ):
        mock_fetch.side_effect = requests.RequestException("Request failed")

        func = fetch_and_cache()
        with pytest.raises(requests.RequestException, match=r"Request failed"):
            func(institution, mock_store)

    assert mock_fetch.call_count == test_config.REQUEST_RETRIES + 1
    mock_set.assert_not_called()
    assert any(
        record.getMessage() == f"Failed to fetch groups from mAP API for institution: {institution.fqdn}"
        for record in log_capture.records
    )


def test_fetch_and_cache_all_redis_error(institutions_data, set_test_config, log_capture):
    data = institutions_data(1)
    institution = Institution(**data[0])
    test_config = set_test_config(REQUEST_RETRY_FACTOR=0, REQUEST_RETRIES=2)
    groups = ["jc_group1", "jc_group2"]

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.fetch_map_groups") as mock_fetch,
        patch("weko_group_cache_db.groups.set_groups_to_redis") as mock_set,
    ):
        mock_fetch.return_value = groups
        mock_set.side_effect = redis.RedisError("Cache error")

        func = fetch_and_cache()
        with pytest.raises(redis.RedisError, match=r"Cache error"):
            func(institution, mock_store)

    assert mock_fetch.call_count == test_config.REQUEST_RETRIES + 1
    assert mock_set.call_count == test_config.REQUEST_RETRIES + 1
    assert any(
        record.getMessage() == f"Failed to cache groups to Redis for institution: {institution.fqdn}"
        for record in log_capture.records
    )


def test_fetch_and_cache_success_after_retries(institutions_data, set_test_config, log_capture):
    data = institutions_data(1)
    institution = Institution(**data[0])
    set_test_config(REQUEST_RETRY_FACTOR=0, REQUEST_RETRIES=2)
    groups = ["jc_group1", "jc_group2"]

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.fetch_map_groups") as mock_fetch,
        patch("weko_group_cache_db.groups.set_groups_to_redis") as mock_set,
    ):
        retries_fetch = 2
        mock_fetch.side_effect = [requests.RequestException("Request failed"), groups, groups]
        retries_set = 1
        mock_set.side_effect = [redis.RedisError("Cache error"), None]

        func = fetch_and_cache()
        count = func(institution, mock_store)

    assert count == len(groups)
    assert mock_fetch.call_count == retries_fetch + 1
    assert mock_set.call_count == retries_set + 1
    assert any(
        record.getMessage() == f"Failed to cache groups to Redis for institution: {institution.fqdn}"
        for record in log_capture.records
    )


def test_fetch_map_groups(institutions_data, set_test_config):
    data = institutions_data(1)
    institution = Institution(**data[0])
    set_test_config()

    response = {
        "totalResults": 2,
        "entry": [
            {"id": "jc_group1", "title": "Group 1"},
            {"id": "jc_group2", "title": "Group 2"},
        ],
    }

    with patch("weko_group_cache_db.groups.requests.get") as mock_get:
        mock_get.return_value.json.return_value = response

        result = fetch_map_groups(institution)
        assert result == ["jc_group1", "jc_group2"]


def test_set_groups_to_redis(institutions_data, set_test_config):
    data = institutions_data(1)
    institution = Institution(**data[0])
    test_config = set_test_config(CACHE_KEY_SUFFIX="_suffix", CACHE_TTL=100)
    timestamp = datetime.now(UTC).isoformat(timespec="seconds")
    groups = ["jc_group1", "jc_group2"]
    transformed_fqdn = institution.fqdn.replace(".", "_").replace("-", "_")
    redis_key = transformed_fqdn + "_suffix"

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection") as mock_conn,
        patch("weko_group_cache_db.groups.datetime") as mock_datetime,
    ):
        mock_datetime.now.return_value.isoformat.return_value = timestamp

        set_groups_to_redis(institution.fqdn, groups, store=mock_store)

    mock_conn.assert_not_called()
    mock_store.hset.assert_called_once_with(redis_key, mapping={"updated_at": timestamp, "groups": ",".join(groups)})
    mock_store.persist.assert_called_once_with(redis_key)
    mock_store.expire.assert_called_once_with(redis_key, test_config.CACHE_TTL)


def test_set_groups_to_redis_no_store(institutions_data, set_test_config):
    data = institutions_data(1)
    institution = Institution(**data[0])
    test_config = set_test_config(CACHE_KEY_SUFFIX="_suffix", CACHE_TTL=100)
    timestamp = datetime.now(UTC).isoformat(timespec="seconds")
    groups = ["jc_group1", "jc_group2"]
    transformed_fqdn = institution.fqdn.replace(".", "_").replace("-", "_")
    redis_key = transformed_fqdn + "_suffix"

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection", return_value=mock_store) as mock_conn,
        patch("weko_group_cache_db.groups.datetime") as mock_datetime,
    ):
        mock_datetime.now.return_value.isoformat.return_value = timestamp

        set_groups_to_redis(institution.fqdn, groups)

    mock_conn.assert_called_once()
    mock_store.hset.assert_called_once_with(redis_key, mapping={"updated_at": timestamp, "groups": ",".join(groups)})
    mock_store.persist.assert_called_once_with(redis_key)
    mock_store.expire.assert_called_once_with(redis_key, test_config.CACHE_TTL)


def test_set_groups_to_redis_no_expire(institutions_data, set_test_config):
    data = institutions_data(1)
    institution = Institution(**data[0])
    set_test_config(CACHE_KEY_SUFFIX="_suffix", CACHE_TTL=-1)
    timestamp = datetime.now(UTC).isoformat(timespec="seconds")
    groups = ["jc_group1", "jc_group2"]
    transformed_fqdn = institution.fqdn.replace(".", "_").replace("-", "_")
    redis_key = transformed_fqdn + "_suffix"

    mock_store = MagicMock()
    with (
        patch("weko_group_cache_db.groups.connection") as mock_conn,
        patch("weko_group_cache_db.groups.datetime") as mock_datetime,
    ):
        mock_datetime.now.return_value.isoformat.return_value = timestamp

        set_groups_to_redis(institution.fqdn, groups, store=mock_store)

    mock_conn.assert_not_called()
    mock_store.hset.assert_called_once_with(redis_key, mapping={"updated_at": timestamp, "groups": ",".join(groups)})
    mock_store.persist.assert_called_once_with(redis_key)
    mock_store.expire.assert_not_called()

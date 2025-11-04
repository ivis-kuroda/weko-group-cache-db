#
# Copyright (C) 2025 National Institute of Informatics.
#

from unittest.mock import patch

from redis.exceptions import RedisError

from weko_group_cache_db.cli import DEFAULT_CONFIG_PATH, DEFAULT_INSTITUTIONS_PATH, run


# def run(file_path: str, config_path: str):
def test_run_no_options(runner):
    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(run)

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_fetch_all.assert_called_once_with(DEFAULT_INSTITUTIONS_PATH)
    assert result.exit_code == 0


def test_run_with_config_path_option(runner, tmp_path):
    test_config_path = tmp_path / "test_config.toml"
    test_config_path.write_text("[settings]\noption = value\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(run, ["--config-path", str(test_config_path)])

    mock_setup_config.assert_called_once_with(str(test_config_path))
    mock_setup_logger.assert_called_once()
    mock_fetch_all.assert_called_once_with(DEFAULT_INSTITUTIONS_PATH)
    assert result.exit_code == 0


def test_run_with_config_path_option_short(runner, tmp_path):
    test_config_path = tmp_path / "test_config.toml"
    test_config_path.write_text("[settings]\noption = value\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(run, ["-c", str(test_config_path)])

    mock_setup_config.assert_called_once_with(str(test_config_path))
    mock_setup_logger.assert_called_once()
    mock_fetch_all.assert_called_once_with(DEFAULT_INSTITUTIONS_PATH)
    assert result.exit_code == 0


def test_run_with_config_path_option_not_exists(runner, tmp_path):
    non_existent_path = tmp_path / "non_existent_config.toml"

    result = runner.invoke(run, ["--config-path", str(non_existent_path)])

    assert result.exit_code != 0
    assert "Invalid value for '--config-path' / '-c'" in result.output
    assert "does not exist." in result.output


def test_run_with_file_path_option(runner, tmp_path):
    test_file_path = tmp_path / "test_institutions.toml"
    test_file_path.write_text("[institutions]\ninst1 = {}\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(run, ["--file-path", str(test_file_path)])

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_fetch_all.assert_called_once_with(str(test_file_path))
    assert result.exit_code == 0


def test_run_with_file_path_option_short(runner, tmp_path):
    test_file_path = tmp_path / "test_institutions.toml"
    test_file_path.write_text("[institutions]\ninst1 = {}\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(run, ["-f", str(test_file_path)])

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_fetch_all.assert_called_once_with(str(test_file_path))
    assert result.exit_code == 0


def test_run_with_file_path_option_not_exists(runner, tmp_path):
    non_existent_path = tmp_path / "non_existent_institutions.toml"

    result = runner.invoke(run, ["--file-path", str(non_existent_path)])
    assert result.exit_code != 0
    assert "Invalid value for '--file-path' / '-f'" in result.output
    assert "does not exist." in result.output


def test_run_fetch_exit_non_zero(runner, tmp_path):
    test_file_path = tmp_path / "test_institutions.toml"
    test_file_path.write_text("[institutions]\ninst1 = {}\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
    ):
        mock_fetch_all.return_value = 1
        result = runner.invoke(run, ["--file-path", str(test_file_path)])

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_fetch_all.assert_called_once_with(str(test_file_path))
    assert result.exit_code == 1


def test_run_fetch_raises_redis_error(runner, tmp_path):
    test_file_path = tmp_path / "test_institutions.toml"
    test_file_path.write_text("[institutions]\ninst1 = {}\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
    ):
        mock_fetch_all.side_effect = RedisError("Redis error")
        result = runner.invoke(run, ["--file-path", str(test_file_path)])

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_fetch_all.assert_called_once_with(str(test_file_path))
    assert result.exit_code != 0

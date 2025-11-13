#
# Copyright (C) 2025 National Institute of Informatics.
#

from unittest.mock import patch

import click
import pytest

from weko_group_cache_db.cli import DEFAULT_CONFIG_PATH, DEFAULT_INSTITUTIONS_PATH, one, run, validate_source_options
from weko_group_cache_db.exc import UpdateError


# def run(file_path: str, directory_path: str, fqdn_list_file: str, config_path: str):
def test_run_no_options(runner, log_capture):
    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(run)

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(None, None, None)
    mock_fetch_all.assert_called_once_with(toml_path=DEFAULT_INSTITUTIONS_PATH)
    assert log_capture.records[0].getMessage() == f"Loading from file source: {DEFAULT_INSTITUTIONS_PATH}"
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "option",
    [
        ("--config-path"),
        ("-c"),
    ],
)
def test_run_with_config_path_option(runner, tmp_path, option, log_capture):
    test_config_path = tmp_path / "test_config.toml"
    test_config_path.write_text("[settings]\noption = value\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(run, [option, str(test_config_path)])

    mock_setup_config.assert_called_once_with(str(test_config_path))
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(None, None, None)
    mock_fetch_all.assert_called_once_with(toml_path=DEFAULT_INSTITUTIONS_PATH)
    assert log_capture.records[0].getMessage() == f"Loading from file source: {DEFAULT_INSTITUTIONS_PATH}"
    assert result.exit_code == 0


def test_run_with_config_path_option_not_exists(runner, tmp_path):
    non_existent_path = tmp_path / "non_existent_config.toml"

    result = runner.invoke(run, ["--config-path", str(non_existent_path)])

    assert result.exit_code != 0
    assert "Invalid value for '--config-path' / '-c'" in result.output
    assert "does not exist." in result.output


@pytest.mark.parametrize(
    "option",
    [
        ("--file-path"),
        ("-f"),
    ],
)
def test_run_with_file_path_option(runner, tmp_path, option, log_capture):
    test_file_path = tmp_path / "test_institutions.toml"
    test_file_path.write_text("[institutions]\nfqdn = example.ac.jp\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(run, [option, str(test_file_path)])

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(str(test_file_path), None, None)
    mock_fetch_all.assert_called_once_with(toml_path=str(test_file_path))
    assert log_capture.records[0].getMessage() == f"Loading from file source: {test_file_path!s}"
    assert result.exit_code == 0


def test_run_with_file_path_option_not_exists(runner, tmp_path):
    non_existent_path = tmp_path / "non_existent_institutions.toml"

    result = runner.invoke(run, ["--file-path", str(non_existent_path)])
    assert result.exit_code != 0
    assert "Invalid value for '--file-path' / '-f'" in result.output
    assert "does not exist." in result.output


@pytest.mark.parametrize(
    ("opt_dir", "opt_list"),
    [
        ("--directory-path", "--fqdn-list-file"),
        ("-d", "-l"),
    ],
    ids=["long-options", "short-options"],
)
def test_run_with_directory_opstions(runner, tmp_path, opt_dir, opt_list, log_capture):
    test_directory_path = tmp_path / "toml_files"
    test_directory_path.mkdir()
    test_fqdn_list_file = tmp_path / "fqdn_list.txt"
    test_fqdn_list_file.write_text("example.ac.jp\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_all.return_value = 0
        result = runner.invoke(
            run,
            [opt_dir, str(test_directory_path), opt_list, str(test_fqdn_list_file)],
        )

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(
        None,
        str(test_directory_path),
        str(test_fqdn_list_file),
    )
    mock_fetch_all.assert_called_once_with(
        directory_path=str(test_directory_path),
        fqdn_list_file=str(test_fqdn_list_file),
    )
    assert (
        log_capture.records[0].getMessage()
        == f"Loading from directory source: {test_directory_path!s} and {test_fqdn_list_file!s}"
    )
    assert result.exit_code == 0


def test_run_fetch_raises_error(runner, tmp_path, log_capture):
    test_file_path = tmp_path / "test_institutions.toml"
    test_file_path.write_text("[institutions]\nfqdn = example.ac.jp\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_all") as mock_fetch_all,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_all.side_effect = ExceptionGroup("Update error", [UpdateError("Fetch error")])
        result = runner.invoke(run, ["--file-path", str(test_file_path)])

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(str(test_file_path), None, None)
    mock_fetch_all.assert_called_once_with(toml_path=str(test_file_path))
    assert log_capture.records[0].getMessage() == f"Loading from file source: {test_file_path!s}"
    assert result.exit_code != 0


# def one(fqdn: str, file_path: str, directory_path: str, fqdn_list_file: str, config_path: str):
def test_one_no_options(runner, log_capture):
    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_one") as mock_fetch_one,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_one.return_value = 0
        result = runner.invoke(one, "example.ac.jp")

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(None, None, None)
    mock_fetch_one.assert_called_once_with("example.ac.jp", toml_path=DEFAULT_INSTITUTIONS_PATH)
    assert log_capture.records[0].getMessage() == f"Loading from file source: {DEFAULT_INSTITUTIONS_PATH}"
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "option",
    [
        ("--config-path"),
        ("-c"),
    ],
)
def test_one_with_config_path_option(runner, tmp_path, option, log_capture):
    test_config_path = tmp_path / "test_config.toml"
    test_config_path.write_text("[settings]\noption = value\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_one") as mock_fetch_one,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_one.return_value = 0
        result = runner.invoke(one, ["example.ac.jp", option, str(test_config_path)])

    mock_setup_config.assert_called_once_with(str(test_config_path))
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(None, None, None)
    mock_fetch_one.assert_called_once_with("example.ac.jp", toml_path=DEFAULT_INSTITUTIONS_PATH)
    assert log_capture.records[0].getMessage() == f"Loading from file source: {DEFAULT_INSTITUTIONS_PATH}"
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "option",
    [
        ("--file-path"),
        ("-f"),
    ],
)
def test_one_with_file_path_option(runner, tmp_path, option, log_capture):
    test_file_path = tmp_path / "test_institutions.toml"
    test_file_path.write_text("[institutions]\nfqdn = example.ac.jp\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_one") as mock_fetch_one,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_one.return_value = 0
        result = runner.invoke(
            one,
            ["example.ac.jp", option, str(test_file_path)],
        )

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(
        str(test_file_path),
        None,
        None,
    )
    mock_fetch_one.assert_called_once_with(
        "example.ac.jp",
        toml_path=str(test_file_path),
    )
    assert log_capture.records[0].getMessage() == f"Loading from file source: {test_file_path!s}"
    assert result.exit_code == 0


@pytest.mark.parametrize(
    ("opt_dir", "opt_list"),
    [
        ("--directory-path", "--fqdn-list-file"),
        ("-d", "-l"),
    ],
    ids=["long-options", "short-options"],
)
def test_one_with_directory_path_option(runner, tmp_path, opt_dir, opt_list, log_capture):
    test_directory_path = tmp_path / "toml_files"
    test_directory_path.mkdir()
    test_fqdn_list_file = tmp_path / "fqdn_list.txt"
    test_fqdn_list_file.write_text("example.ac.jp\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_one") as mock_fetch_one,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_one.return_value = 0
        result = runner.invoke(
            one,
            [
                "example.ac.jp",
                opt_dir,
                str(test_directory_path),
                opt_list,
                str(test_fqdn_list_file),
            ],
        )

    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(
        None,
        str(test_directory_path),
        str(test_fqdn_list_file),
    )
    mock_fetch_one.assert_called_once_with(
        "example.ac.jp",
        directory_path=str(test_directory_path),
        fqdn_list_file=str(test_fqdn_list_file),
    )
    assert (
        log_capture.records[0].getMessage()
        == f"Loading from directory source: {test_directory_path!s} and {test_fqdn_list_file!s}"
    )
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "error_instance",
    [
        ValueError("Institution not found"),
        UpdateError("Fetch error"),
    ],
    ids=["ValueError", "UpdateError"],
)
def test_one_fetch_raises_error(runner, tmp_path, error_instance, log_capture):
    test_file_path = tmp_path / "test_institutions.toml"
    test_file_path.write_text("[institutions]\nfqdn = example.ac.jp\n")

    with (
        patch("weko_group_cache_db.cli.setup_config") as mock_setup_config,
        patch("weko_group_cache_db.cli.setup_logger") as mock_setup_logger,
        patch("weko_group_cache_db.cli.fetch_one") as mock_fetch_one,
        patch("weko_group_cache_db.cli.validate_source_options") as mock_validate_source_options,
    ):
        mock_fetch_one.side_effect = error_instance
        result = runner.invoke(
            one,
            ["example.ac.jp", "--file-path", str(test_file_path)],
        )
    mock_setup_config.assert_called_once_with(DEFAULT_CONFIG_PATH)
    mock_setup_logger.assert_called_once()
    mock_validate_source_options.assert_called_once_with(
        str(test_file_path),
        None,
        None,
    )
    mock_fetch_one.assert_called_once_with(
        "example.ac.jp",
        toml_path=str(test_file_path),
    )
    assert log_capture.records[0].getMessage() == f"Loading from file source: {test_file_path!s}"
    assert result.exit_code != 0


@pytest.mark.parametrize(
    ("file_path", "directory_path", "fqdn_list_file"),
    [
        (None, None, None),
        ("path/to/file.toml", None, None),
        (None, "path/to/directory", "path/to/fqdn_list.txt"),
    ],
    ids=["no-options", "only-file-path", "directory-and-list"],
)
def test_validate_source_options_pass(file_path, directory_path, fqdn_list_file):
    # Should not raise any exception
    validate_source_options(file_path, directory_path, fqdn_list_file)


@pytest.mark.parametrize(
    ("file_path", "directory_path", "fqdn_list_file", "error_type"),
    [
        ("path/to/file.toml", "path/to/directory", None, "Cannot specify both"),
        ("path/to/file.toml", None, "path/to/fqdn_list.txt", "Cannot specify both"),
        (None, "path/to/directory", None, "Both must be specified"),
        (None, None, "path/to/fqdn_list.txt", "Both must be specified"),
        ("path/to/file.toml", "path/to/directory", "path/to/fqdn_list.txt", "Cannot specify both"),
    ],
    ids=[
        "file-and-directory",
        "file-and-list",
        "only-directory",
        "only-fqdn-list",
        "all-options",
    ],
)
def test_validate_source_options_fail(file_path, directory_path, fqdn_list_file, error_type):
    with pytest.raises(click.UsageError) as exc_info:
        validate_source_options(file_path, directory_path, fqdn_list_file)

    message = (
        "Cannot specify both --file-path and --directory-path/--fqdn-list-file."
        if error_type == "Cannot specify both"
        else "Both --directory-path and --fqdn-list-file must be specified."
    )

    assert exc_info.value.message == message

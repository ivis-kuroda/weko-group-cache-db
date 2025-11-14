#
# Copyright (C) 2025 National Institute of Informatics.
#

from tomllib import TOMLDecodeError
from unittest.mock import patch

import pytest

from pydantic_core import ValidationError

from weko_group_cache_db import loader
from weko_group_cache_db.exc import ConfigurationError
from weko_group_cache_db.loader import (
    Institution,
    check_existence_file,
    load_institutions,
    load_institutions_from_directory,
    load_institutions_from_toml,
)


# def load_institutions(**kwargs: t.Unpack[InstitutionSource]) -> list[Institution]:
def test_load_institutions_toml():
    with patch("weko_group_cache_db.loader.load_institutions_from_toml") as mock_load:
        load_institutions(toml_path="institutions.toml")

    mock_load.assert_called_once_with("institutions.toml")


def test_load_institutions_directory():
    with patch("weko_group_cache_db.loader.load_institutions_from_directory") as mock_load:
        load_institutions(directory_path="institutions", fqdn_list_file="fqdn_list.txt")

    mock_load.assert_called_once_with("institutions", "fqdn_list.txt")


def test_load_institutions_invalid(log_capture):
    with (
        patch("weko_group_cache_db.loader.load_institutions_from_toml") as mock_load_toml,
        patch("weko_group_cache_db.loader.load_institutions_from_directory") as mock_load_directory,
    ):
        load_institutions()

    mock_load_toml.assert_not_called()
    mock_load_directory.assert_not_called()
    assert log_capture.records[0].getMessage() == "Invalid institution source configuration."


# def load_institutions_from_toml(toml_path: str | Path) -> list[Institution]:
def test_load_institutions_from_toml(tmp_path, institutions_data, log_capture):
    num_institutions = 2
    toml_path = tmp_path / "test_institutions.toml"
    toml_path.write_text("[[institutions]]\n")
    data = institutions_data(num_institutions)

    with (
        patch("weko_group_cache_db.loader.tomllib.load") as mock_load,
        patch("weko_group_cache_db.loader.check_existence_file") as mock_check,
    ):
        mock_load.return_value = {"institutions": data}
        mock_check.return_value = True

        result = load_institutions_from_toml(toml_path)

    assert len(result) == num_institutions
    assert all(isinstance(inst, Institution) for inst in result)
    assert result[0].model_dump() == data[0]
    assert result[1].model_dump() == data[1]
    assert log_capture.records[0].getMessage() == f"{num_institutions} institutions loaded successfully."


def test_load_institutions_from_toml_alias(tmp_path, institutions_data, institutions_data_alias, log_capture):
    num_institutions = 2
    toml_path = tmp_path / "test_institutions_alias.toml"
    toml_path.write_text("[[institutions]]\n")
    base_data = institutions_data(num_institutions)
    data = institutions_data_alias(num_institutions)

    with (
        patch("weko_group_cache_db.loader.tomllib.load") as mock_load,
        patch("weko_group_cache_db.loader.check_existence_file") as mock_check,
    ):
        mock_load.return_value = {"institutions": data}
        mock_check.return_value = True

        result = load_institutions_from_toml(toml_path)

    assert len(result) == num_institutions
    assert all(isinstance(inst, Institution) for inst in result)
    assert result[0].model_dump() == base_data[0]
    assert result[1].model_dump() == base_data[1]
    assert log_capture.records[0].getMessage() == f"{num_institutions} institutions loaded successfully."


def test_load_institutions_from_toml_no_sections(tmp_path, institutions_data, log_capture):
    num_institutions = 2
    toml_path = tmp_path / "test_institutions.toml"
    toml_path.write_text("[[institutions]]\n")
    data = institutions_data(num_institutions)

    with (
        patch("weko_group_cache_db.loader.tomllib.load") as mock_load,
        patch("weko_group_cache_db.loader.check_existence_file") as mock_check,
    ):
        mock_load.return_value = {"invalid_section": data}

        result = load_institutions_from_toml(toml_path)

    assert len(result) == 0
    assert log_capture.records[0].getMessage() == "No 'institutions' section found in the TOML file."
    mock_check.assert_not_called()


def test_load_institutions_from_toml_no_list(tmp_path, institutions_data, log_capture):
    num_institutions = 1
    toml_path = tmp_path / "test_institutions.toml"
    toml_path.write_text("[[institutions]]\n")
    data = institutions_data(num_institutions)

    with (
        patch("weko_group_cache_db.loader.tomllib.load") as mock_load,
        patch("weko_group_cache_db.loader.check_existence_file") as mock_check,
    ):
        mock_load.return_value = {"institutions": data[0]}
        mock_check.return_value = True

        result = load_institutions_from_toml(toml_path)

    assert len(result) == 0
    assert log_capture.records[0].getMessage() == "The 'institutions' section must be a list in the TOML file."
    mock_check.assert_not_called()


def test_load_institutions_from_toml_file_not_found(log_capture):
    toml_path = "non_existent.toml"

    with pytest.raises(ConfigurationError):
        load_institutions_from_toml(toml_path)

    assert log_capture.records[0].getMessage() == f"TOML file not found: {toml_path}"


def test_load_institutions_from_toml_decode_error(tmp_path, log_capture):
    toml_path = tmp_path / "invalid.toml"
    toml_path.write_text("invalid toml content")

    with patch("weko_group_cache_db.loader.tomllib.load") as mock_load:
        mock_load.side_effect = TOMLDecodeError("Invalid TOML", toml_path, 0)

        with pytest.raises(ConfigurationError):
            load_institutions_from_toml(toml_path)

    assert log_capture.records[0].getMessage() == f"Failed to load TOML file: {toml_path}"


def test_load_institutions_from_toml_validation_error(tmp_path, institutions_data, log_capture):
    toml_path = tmp_path / "test_institutions.toml"
    toml_path.write_text("[[institutions]]\n")
    data = institutions_data(2)
    data[1].pop("fqdn")  # Remove required field to cause validation error

    with (
        patch("weko_group_cache_db.loader.tomllib.load") as mock_load,
        patch("weko_group_cache_db.loader.check_existence_file") as mock_check,
    ):
        mock_load.return_value = {"institutions": data}
        mock_check.return_value = True

        result = load_institutions_from_toml(toml_path)

    assert len(result) == 1
    assert all(isinstance(inst, Institution) for inst in result)
    assert result[0].model_dump() == data[0]
    assert log_capture.records[0].getMessage() == 'Failed to load 2nd institution "Unknown".'
    assert log_capture.records[1].getMessage() == "1 institutions loaded successfully."


def test_load_institutions_from_toml_no_crt(log_capture, tmp_path, institutions_data):
    toml_path = tmp_path / "test_institutions.toml"
    toml_path.write_text("[[institutions]]\n")
    data = institutions_data(2)

    with (
        patch("weko_group_cache_db.loader.tomllib.load") as mock_load,
        patch("weko_group_cache_db.loader.check_existence_file") as mock_check,
    ):
        mock_load.return_value = {"institutions": data}
        mock_check.side_effect = [True, False]

        result = load_institutions_from_toml(toml_path)

    assert len(result) == 1
    assert all(isinstance(inst, Institution) for inst in result)
    assert result[0].model_dump() == data[0]
    assert (
        log_capture.records[0].getMessage()
        == 'Skip 2nd institution "example2.ac.jp" due to missing TLS client cert/key files.'
    )
    assert log_capture.records[1].getMessage() == "1 institutions loaded successfully."


def test_load_institutions_from_directory(tmp_path, institutions_data, log_capture, set_test_config):
    directory_path = tmp_path / "institutions"
    directory_path.mkdir()
    fqdn_list_file = tmp_path / "fqdn_list.txt"
    num_institutions = 2
    data = institutions_data(num_institutions)

    fqdn_list_file.write_text("\n".join([inst["fqdn"] for inst in data]))

    set_test_config(SP_CONNECTOR_ID_PREFIX="test_jc_")

    with patch("weko_group_cache_db.loader.check_existence_file") as mock_check:
        mock_check.return_value = True

        result = load_institutions_from_directory(directory_path, fqdn_list_file)

    assert len(result) == num_institutions
    assert all(isinstance(inst, Institution) for inst in result)
    assert result[0].fqdn == data[0]["fqdn"]
    assert result[0].sp_connector_id == data[0]["sp_connector_id"]
    assert result[0].client_cert_path == str(directory_path / data[0]["fqdn"] / loader.CRT_FILE_NAME)
    assert result[1].fqdn == data[1]["fqdn"]
    assert result[1].sp_connector_id == data[1]["sp_connector_id"]
    assert result[1].client_cert_path == str(directory_path / data[1]["fqdn"] / loader.CRT_FILE_NAME)
    assert log_capture.records[0].getMessage() == f"{num_institutions} institutions loaded successfully."


def test_load_institutions_from_directory_validation_error(tmp_path, institutions_data, log_capture):
    directory_path = tmp_path / "institutions"
    directory_path.mkdir()
    fqdn_list_file = tmp_path / "fqdn_list.txt"
    num_institutions = 2
    data = institutions_data(num_institutions)

    fqdn_list_file.write_text("\n".join([inst["fqdn"] for inst in data]))

    with (
        patch("weko_group_cache_db.loader.Institution") as mock_validate,
        patch("weko_group_cache_db.loader.check_existence_file") as mock_check,
    ):
        validation_error = ValidationError.from_exception_data(
            "test",
            [{"loc": ("fqdn",), "input": "test", "type": "value_error", "ctx": {"error": "test"}}],
        )
        mock_validate.side_effect = validation_error
        mock_check.return_value = True

        result = load_institutions_from_directory(str(directory_path), fqdn_list_file)

    assert len(result) == 0
    assert log_capture.records[0].getMessage() == f'Failed to load 1st institution "{data[0]["fqdn"]}".'
    assert log_capture.records[1].getMessage() == f'Failed to load 2nd institution "{data[1]["fqdn"]}".'
    assert log_capture.records[2].getMessage() == "0 institutions loaded successfully."


def test_load_institutions_from_directory_no_cert(tmp_path, institutions_data, log_capture):
    directory_path = tmp_path / "institutions"
    directory_path.mkdir()
    fqdn_list_file = tmp_path / "fqdn_list.txt"
    num_institutions = 2
    data = institutions_data(num_institutions)

    fqdn_list_file.write_text("\n".join([inst["fqdn"] for inst in data]))

    with patch("weko_group_cache_db.loader.check_existence_file") as mock_check:
        mock_check.side_effect = [True, False]

        result = load_institutions_from_directory(directory_path, str(fqdn_list_file))

    assert len(result) == 1
    assert (
        log_capture.records[0].getMessage()
        == f'Skip 2nd institution "{data[1]["fqdn"]}" due to missing TLS client cert/key files.'
    )
    assert log_capture.records[1].getMessage() == "1 institutions loaded successfully."


# def check_existence_file(institution: Institution) -> bool:
def test_check_existence_file(tmp_path):
    cert_path = tmp_path / "client_cert.pem"
    key_path = tmp_path / "client_key.pem"

    cert_path.write_text("dummy_cert_content")
    key_path.write_text("dummy_key_content")

    institution = Institution(
        name="Test Institution",
        fqdn="test.institution",
        sp_connector_id="test_institution",
        client_cert_path=str(cert_path),
        client_key_path=str(key_path),
    )
    assert check_existence_file(institution) is True


def test_check_existence_cert_not_exist(tmp_path):
    cert_path = tmp_path / "client_cert.pem"
    key_path = tmp_path / "client_key.pem"

    key_path.write_text("dummy_key_content")

    institution = Institution(
        name="Test Institution",
        fqdn="test.institution",
        sp_connector_id="test_institution",
        client_cert_path=str(cert_path),
        client_key_path=str(key_path),
    )
    assert check_existence_file(institution) is False


def test_check_existence_key_not_exist(tmp_path):
    cert_path = tmp_path / "client_cert.pem"
    key_path = tmp_path / "client_key.pem"

    cert_path.write_text("dummy_cert_content")

    institution = Institution(
        name="Test Institution",
        fqdn="test.institution",
        sp_connector_id="test_institution",
        client_cert_path=str(cert_path),
        client_key_path=str(key_path),
    )
    assert check_existence_file(institution) is False


def test_check_existence_files_not_exist(tmp_path):
    cert_path = tmp_path / "client_cert.pem"
    key_path = tmp_path / "client_key.pem"

    institution = Institution(
        name="Test Institution",
        fqdn="test.institution",
        sp_connector_id="test_institution",
        client_cert_path=str(cert_path),
        client_key_path=str(key_path),
    )
    assert check_existence_file(institution) is False

#
# Copyright (C) 2025 National Institute of Informatics.
#

from weko_group_cache_db.loader import Institution, check_existence_file


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

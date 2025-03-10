import pytest
from logging import  ERROR, INFO
from get_groups.tasks import create_set_groups_task, set_groups_task
from unittest.mock import patch, MagicMock


def test_07_create_set_groups_task(test_logger):
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        create_set_groups_task()
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]

    assert 'All set_groups_task are created.' == info_logs[0]


def test_08_create_set_groups_task(test_logger):
    with patch('config.config.SP_AUTHORIZATION_DICT', data_2):
        with pytest.raises(Exception):
            create_set_groups_task()
        error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]

        assert 'Error occurred in create_set_groups_task.' == error_logs[0]


def test_09_set_groups_task(test_logger):
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "totalResults" : 1,
                "entry" : [
                    {
                        "id" : "https:\/\/cg.gakunin.jp\/gr\/GakuNinTF",
                        "title" : "group",
                        "description" : "group-test",
                        "map_totalMembers" : 1
                    },
                ]
            }
            mock_get.return_value = mock_response
            set_groups_task('org.idp.co,jp')
            info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]

        assert 'FQDN(org.idp.co,jp) is success.' == info_logs[0]


def test_10_set_groups_task(test_logger):
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "totalResults" : 1,
                "entry" : [
                    {
                        "id" : "https:\/\/cg.gakunin.jp\/gr\/GakuNinTF",
                        "title" : "group",
                        "description" : "group-test",
                        "map_totalMembers" : 1
                    },
                ]
            }
            mock_get.return_value = mock_response
            with pytest.raises(Exception):
                set_groups_task('XXXX')
            error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]

            assert 'FQDN(XXXX) is failed.' == error_logs[0]


data = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
    'Organization Name2': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
    'Organization Name3': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}


data_2 = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
    },
}
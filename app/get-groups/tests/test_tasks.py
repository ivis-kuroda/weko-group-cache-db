from logging import ERROR, INFO
from unittest.mock import MagicMock, patch

import pytest

from get_groups.tasks import create_set_groups_task, set_groups_task

# def create_set_groups_task():
# .tox/c1/bin/pytest --cov=get_groups tests/test_tasks.py::test_07_create_set_groups_task -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "All set_groups_task are created." is logged.
def test_07_create_set_groups_task(test_logger, prepare_authorization_dict):
    with patch('config.config.SP_AUTHORIZATION_DICT', prepare_authorization_dict):
        with patch('get_groups.tasks.set_groups_task') as mock_set_groups_task:
            create_set_groups_task()

            info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
            assert 'All set_groups_task are created.' == info_logs[0]

# def create_set_groups_task():
# .tox/c1/bin/pytest --cov=get_groups tests/test_tasks.py::test_08_create_set_groups_task -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "Error occurred in create_set_groups_task." is logged.
def test_08_create_set_groups_task(test_logger, prepare_authorization_dict):
    key_name = 'Organization Name'
    prepare_authorization_dict[key_name].pop('org_sp_fqdn')
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
        create_set_groups_task()

        error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]
        assert 'FQDN is not defined in config for Organization Name.' == error_logs[0]
    
    with patch('config.config.SP_AUTHORIZATION_DICT', prepare_authorization_dict):
        with patch('get_groups.tasks.set_groups_task.delay', side_effect=Exception('Test Exception')):
            with pytest.raises(Exception):
                create_set_groups_task()
            error_logs = test_logger.record_tuples[-1][2]
            assert 'Error occurred in create_set_groups_task.' == error_logs

# def set_groups_task(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_tasks.py::test_09_set_groups_task -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "FQDN([fqdn]) is success." is logged.
def test_09_set_groups_task(test_logger, prepare_authorization_dict):
    with patch('config.config.SP_AUTHORIZATION_DICT', prepare_authorization_dict):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "totalResults" : 1,
                "entry" : [
                    {
                        "id" : "https://cg.gakunin.jp/gr/GakuNinTF",
                        "title" : "group",
                        "description" : "group-test",
                        "map_totalMembers" : 1
                    },
                ]
            }
            mock_get.return_value = mock_response
            
            target_fqdn = 'org.sp.co.jp'
            set_groups_task(target_fqdn)
 
            info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
            assert 'FQDN({}) is success.'.format(target_fqdn) == info_logs[0]

# def set_groups_task(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_tasks.py::test_10_set_groups_task -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "FQDN([fqdn]) is failed." is logged.
def test_10_set_groups_task(test_logger, prepare_authorization_dict):
    with patch('config.config.SP_AUTHORIZATION_DICT', prepare_authorization_dict):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "totalResults" : 1,
                "entry" : [
                    {
                        "id" : "https://cg.gakunin.jp/gr/GakuNinTF",
                        "title" : "group",
                        "description" : "group-test",
                        "map_totalMembers" : 1
                    },
                ]
            }
            mock_get.return_value = mock_response

            target_fqdn = 'XXXX'
            with pytest.raises(Exception):
                set_groups_task(target_fqdn)

            error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]
            assert 'FQDN({}) is failed.'.format(target_fqdn) == error_logs[0]

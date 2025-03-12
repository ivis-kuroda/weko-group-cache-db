from logging import ERROR
from unittest.mock import patch

from new_group.api import set_new_group_id

# def set_new_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_api.py::test_01_set_new_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# json of the success pattern is returned.
def test_01_set_new_group_id(app, prepare_authorization_dict):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        result = set_new_group_id('jc_test_org_groups_example')
        
        assert result.json == {"result": "OK","message": "Success."}

# def set_new_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_api.py::test_02_set_new_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# json of the failure pattern is returned.
def test_02_set_new_group_id(app, test_logger):
    with patch('new_group.api.set_group_id', side_effect=Exception("Test Exception occurred.")):
        result = set_new_group_id('jc_test_org_groups_example')

        error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]
        assert result.json == {"result": "NG", "message": 'Test Exception occurred.'}
        assert 'Test Exception occurred.' == error_logs[0]

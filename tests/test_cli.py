
from logging import ERROR, INFO
from unittest.mock import MagicMock, patch

from config import CLI_LOG_OUTPUT_PATH
from cli import get_groups

# def get_groups(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_cli.py::test_01_get_groups -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "[fqdn] is success." is standard output.
# "[fqdn] is success." is logged.
def test_01_get_groups(runner, test_logger, prepare_authorization_dict):
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
            result = runner.invoke(get_groups, ['--fqdn', target_fqdn])

            info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
            assert "{} is success.\n".format(target_fqdn) == result.output
            assert "{} is success.".format(target_fqdn) == info_logs[0]

# def get_groups(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_cli.py::test_02_get_groups -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "[fqdn] is success." is stdout.
# "[fqdn] is success." is logged.
def test_02_get_groups(runner, test_logger, prepare_authorization_dict):
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
            result = runner.invoke(get_groups, ['-f', target_fqdn]) 

            info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
            assert "{} is success.\n".format(target_fqdn) == result.output
            assert "{} is success.".format(target_fqdn) == info_logs[0]

# def get_groups(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_cli.py::test_03_get_groups -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "[fqdn] is failed: FQDN is not found in config." is stdout.
# "For details, see [log_file]." is stdout.
# "FQDN is not found in config." is output to config.CLI_LOG_OUTPUT_PATH.
def test_03_get_groups(runner, test_logger, prepare_authorization_dict):
    with patch('config.config.SP_AUTHORIZATION_DICT', prepare_authorization_dict):
        target_fqdn = 'XXXXXXXX'
        result = runner.invoke(get_groups, ['--fqdn', target_fqdn])

        error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]
        assert "{0} is failed: FQDN({0}) is not found in config.\nFor details, see {1}.\n"\
            .format(target_fqdn, CLI_LOG_OUTPUT_PATH) == result.output
        assert "FQDN({}) is not found in config.".format(target_fqdn) == error_logs[0]

# def get_groups(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_cli.py::test_04_get_groups -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "[fqdn] is failed: [fqdn] is not found in config." is stdout.
# "For details, see [log_file]." is stdout.
# "[fqdn] is not found in config." is output to config.CLI_LOG_OUTPUT_PATH.
def test_04_get_groups(runner, test_logger, prepare_authorization_dict):
    with patch('config.config.SP_AUTHORIZATION_DICT', prepare_authorization_dict):
        target_fqdn = 'XXXXXXXX'
        result = runner.invoke(get_groups, ['-f', target_fqdn])

        error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]
        assert "{0} is failed: FQDN({0}) is not found in config.\nFor details, see {1}.\n"\
            .format(target_fqdn, CLI_LOG_OUTPUT_PATH) == result.output
        assert "FQDN({}) is not found in config.".format(target_fqdn) == error_logs[0]

# def get_groups(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_cli.py::test_05_get_groups -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# An error message stating that the “--fqdn” option is missing.
def test_05_get_groups(runner):
    result = runner.invoke(get_groups)

    assert result.exit_code == 2
    assert "Error: Missing option \'-f\' / \'--fqdn\'" in result.output

# def get_groups(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_cli.py::test_06_get_groups -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# An error message stating that the option “--org” does not exist.
def test_06_get_groups(runner):
    result = runner.invoke(get_groups, ['--fqdn', 'org.sp.co.jp', '--org', 'test_org'])

    assert result.exit_code == 2
    assert 'Error: No such option: {}'.format('--org') in result.output     

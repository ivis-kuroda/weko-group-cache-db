
from logging import ERROR, INFO
from get_groups.cli import get_groups
from config.config import CLI_LOG_OUTPUT_PATH
from unittest.mock import patch, MagicMock

def test_01_get_groups(runner, test_logger):
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
            result = runner.invoke(get_groups, ['--fqdn', 'org.idp.co,jp'])
            info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]

            assert "{} is success.\n".format("org.idp.co,jp") == result.output
            assert "{} is success.".format("org.idp.co,jp") == info_logs[0]


def test_02_get_groups(runner, test_logger):
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
            result = runner.invoke(get_groups, ['-f', 'org.idp.co,jp']) 
            info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]

            assert "{} is success.\n".format("org.idp.co,jp") == result.output
            assert "{} is success.".format("org.idp.co,jp") == info_logs[0]


def test_03_get_groups(runner, test_logger):
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        result = runner.invoke(get_groups, ['--fqdn', 'XXXXXXXX'])

        assert "{0} is failed: FQDN({0}) is not found in config.\nFor details, see {1}.\n".format("XXXXXXXX", CLI_LOG_OUTPUT_PATH) == result.output
        error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]
        assert "FQDN({}) is not found in config.".format("XXXXXXXX") == error_logs[0]


def test_04_get_groups(runner, test_logger):
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        result = runner.invoke(get_groups, ['-f', 'XXXXXXXX'])

        assert "{0} is failed: FQDN({0}) is not found in config.\nFor details, see {1}.\n".format("XXXXXXXX", CLI_LOG_OUTPUT_PATH) == result.output
        error_logs = [record[2] for record in test_logger.record_tuples if record[1] == ERROR]
        assert "FQDN({}) is not found in config.".format("XXXXXXXX") == error_logs[0]


def test_05_get_groups(runner):
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        result = runner.invoke(get_groups)

        assert result.exit_code == 2
        assert "Error: Missing option \'-f\' / \'--fqdn\'" in result.output


def test_06_get_groups(runner):
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        result = runner.invoke(get_groups, ['--fqdn', 'org.idp.co,jp', '--org test_org'])

        assert result.exit_code == 2
        assert 'Error: No such option: {}'.format('--org test_org') in result.output     

data = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}
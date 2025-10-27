import os
import subprocess
from logging import INFO

import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner

@pytest.fixture
def runner():
    """Fixture for invoking command-line interfaces.
    
    Returns:
        CliRunner: A CliRunner instance.
    """
    return CliRunner()

@pytest.fixture
def test_logger(caplog: LogCaptureFixture):
    """Fixture for capturing logs.
    
    Args:
        caplog (LogCaptureFixture): A LogCaptureFixture instance.
        
    Returns:
        LogCaptureFixture: A LogCaptureFixture instance.
    """
    caplog.set_level(INFO)
    return caplog

@pytest.fixture
def prepare_authorization_dict():
    """Fixture for preparing a dictionary of authorization information.
    
    Returns:
        dict: A dictionary of authorization information.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    function_dir = current_dir.split('app')[0]
    cert_file = os.path.join(function_dir, 'nginx/keys/server.crt')
    key_file = os.path.join(function_dir, 'nginx/keys/server.key')
    return {
        'Organization Name': {
            'sp_connector_id': 'connector1',
            'tls_client_cert': cert_file,
            'tls_client_key': key_file,
            'org_sp_fqdn': 'org.sp.co.jp'
        },
        'Organization Name2': {
            'sp_connector_id': 'connector2',
            'tls_client_cert': cert_file,
            'tls_client_key': key_file,
            'org_sp_fqdn': 'org.sp2.co.jp'
        },
        'Organization Name3': {
            'sp_connector_id': 'connector3',
            'tls_client_cert': cert_file,
            'tls_client_key': key_file,
            'org_sp_fqdn': 'org.sp3.co.jp'
        }
    }


@pytest.fixture
def switch_to_sentinel():
    """Switch to sentinel for testing
    
    This fixture stops the redis container and starts the sentinel container
    for testing purposes. It will switch back to the redis container after the
    test is complete.
    """
    subprocess.run(['docker', 'compose', 'stop', 'redis'])
    subprocess.run(['docker', 'compose', '-f', '../../docker-compose-sentinel.yml', 'up', '-d'])
    yield
    subprocess.run(['docker', 'compose', '-f', '../../docker-compose-sentinel.yml', 'down'])
    subprocess.run(['docker', 'compose', 'start', 'redis'])


import os
from logging import INFO

import pytest
from _pytest.logging import LogCaptureFixture
from flask import Flask

from config.config import GROUPS_DB
from jc_redis.redis_conn import RedisConnection

@pytest.fixture
def app():
    app = Flask(__name__)
    with app.app_context():
        yield app

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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    function_dir = current_dir.split('app')[0]
    key_file = os.path.join(function_dir, 'nginx/keys/server.crt')
    return {
        'Organization Name': {
            'sp_connector_id': 'connector1',
            'tls_client_cert': key_file,
            'org_sp_fqdn': 'test.org'
        }
    }

@pytest.fixture
def prepare_redis_connection():
    store = RedisConnection().connection(GROUPS_DB)
    store.flushdb()
    yield store
    store.flushdb()
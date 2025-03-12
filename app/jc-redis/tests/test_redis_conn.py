import subprocess
from unittest.mock import patch

import pytest
import redis

from jc_redis.redis_conn import RedisConnection

# def __init__(self):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_23___init__ -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# redis_type of the created instance is "redis"
def test_23___init__():
    assert RedisConnection().redis_type == 'redis'

# def __init__(self):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_24___init__ -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# redis_type of the created instance is "sentinel"
def test_24___init__():
    with patch('config.config.CACHE_TYPE', 'sentinel'):    
        assert RedisConnection().redis_type == 'sentinel'

# def connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_25_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_25_connection():
    store = RedisConnection().connection(0)

    assert isinstance(store, redis.StrictRedis)

# def connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_26_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_26_connection():
    with patch('config.config.CACHE_TYPE', 'sentinel'):
        store = RedisConnection().connection(0)

    assert isinstance(store, redis.StrictRedis)

# def connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_27_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# None is returned
def test_27_connection():
    with patch('config.config.CACHE_TYPE', 'test'):
        result = RedisConnection().connection(0)

    assert result == None
    
# def connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_28_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_28_connection():
    store = RedisConnection().connection(16)

    assert isinstance(store, redis.StrictRedis)

# def connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_29_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Exception is raised
def test_29_connection():
    with patch('jc_redis.redis_conn.RedisConnection.redis_connection') as mock_redis_connection:
        mock_redis_connection.side_effect = Exception('Test Error')
        with pytest.raises(Exception) as exc_info:
            RedisConnection().connection(0)

        assert str(exc_info.value) == 'Test Error'

# def redis_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_30_redis_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_30_redis_connection():
    store = RedisConnection().redis_connection(0)

    assert isinstance(store, redis.StrictRedis)

# def redis_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_31_redis_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_31_redis_connection():
    store = RedisConnection().redis_connection(16)

    assert isinstance(store, redis.StrictRedis)

# def redis_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_32_redis_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_32_redis_connection():
    subprocess.run(['docker', 'compose', 'stop', 'redis'])
    store = RedisConnection().redis_connection(0)

    assert isinstance(store, redis.StrictRedis)
    subprocess.run(['docker', 'compose', 'start', 'redis'])

# def redis_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_33_redis_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_33_redis_connection(switch_to_sentinel):
    store = RedisConnection().redis_connection(0)

    assert isinstance(store, redis.StrictRedis)

# def redis_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_34_redis_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_34_redis_connection():
    with patch('config.config.REDIS_URL', 'redis://redis-test:6379/') as mock_redis_url:
        store = RedisConnection().redis_connection(0)

        assert isinstance(store, redis.StrictRedis)

# def redis_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_35_redis_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Exception is raised
def test_35_redis_connection():
    with patch('redis.StrictRedis.from_url') as mock_from_url:
        mock_from_url.side_effect = Exception('Test Error')
        with pytest.raises(Exception) as exc_info:
            RedisConnection().redis_connection(0)

        assert str(exc_info.value) == 'Test Error'

# def sentinel_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_36_sentinel_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_36_sentinel_connection(switch_to_sentinel):
    store = RedisConnection().sentinel_connection(0)

    assert isinstance(store, redis.StrictRedis)

# def sentinel_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_37_sentinel_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_37_sentinel_connection(switch_to_sentinel):
    store = RedisConnection().sentinel_connection(16)

    assert isinstance(store, redis.StrictRedis)

# def sentinel_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_38_sentinel_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_38_sentinel_connection():
    subprocess.run(['docker', 'compose', 'stop', 'redis'])
    store = RedisConnection().sentinel_connection(0)

    assert isinstance(store, redis.StrictRedis)
    subprocess.run(['docker', 'compose', 'start', 'redis'])

# def sentinel_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_39_sentinel_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_39_sentinel_connection():
    store = RedisConnection().sentinel_connection(0)

    assert isinstance(store, redis.StrictRedis)

# def sentinel_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_40_sentinel_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Redis store object is returned
def test_40_sentinel_connection(switch_to_sentinel):
    with patch('config.config.CACHE_REDIS_SENTINELS', [('localhost', 26379)]) as mock_sentinels:
        store = RedisConnection().sentinel_connection(0)

        assert isinstance(store, redis.StrictRedis)

# def sentinel_connection(self, db):
# .tox/c1/bin/pytest --cov=jc_redis tests/test_redis_conn.py::test_41_sentinel_connection -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Exception is raised
def test_41_sentinel_connection(switch_to_sentinel):
    with patch('redis.sentinel.Sentinel.master_for') as mock_sentinel:
        mock_sentinel.side_effect = Exception('Test Error')
        with pytest.raises(Exception) as exc_info:
            RedisConnection().sentinel_connection(0)

        assert str(exc_info.value) == 'Test Error'
    
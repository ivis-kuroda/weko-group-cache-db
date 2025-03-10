import redis
import pytest
from redis.exceptions import ResponseError
from jc_redis.redis import RedisConnection
from unittest.mock import patch



@pytest.fixture
def redis_client():
    return redis.StrictRedis(host='localhost', port=6379, db=0)


def test_23___init__():
    assert RedisConnection().redis_type == 'redis'


def test_24___init__():
    with patch('config.config.CACHE_TYPE', 'sentinel'):    
        assert RedisConnection().redis_type == 'sentinel'


def test_25_connection():
    store = RedisConnection().connection(0)

    assert isinstance(store, redis.StrictRedis)
    # assert store.connection_pool.get_connection('').host == 'localhost'
    # assert store.connection_pool.get_connection('').port == 6379
    # assert store.connection_pool.get_connection('').db == db


def test_26_connection():
    with patch('config.config.CACHE_TYPE', 'sentinel'):
        store = RedisConnection().connection(0)

    assert isinstance(store, redis.StrictRedis)


def test_27_connection():
    with patch('config.config.CACHE_TYPE', 'test'):
        result = RedisConnection().connection(0)

    assert result == None
    

def test_28_connection(redis_client):
    with pytest.raises(ResponseError)  as exc_info:
        redis_client.execute_command('SELECT', 16)

    assert str(exc_info.value) == "DB index is out of range" 


def test_29_redis_connection():
    db = 0
    store = RedisConnection().connection(db)

    assert isinstance(store, redis.StrictRedis)
    assert store.connection_pool.get_connection('').host == 'localhost'
    assert store.connection_pool.get_connection('').port == 6379
    assert store.connection_pool.get_connection('').db == db


def test_30_redis_connection(redis_client):
    with pytest.raises(ResponseError)  as exc_info:
        redis_client.execute_command('SELECT', 16)

    assert str(exc_info.value) == "DB index is out of range" 


def test_34_sentinel_connection():
    db = 0
    store = RedisConnection().connection(db)

    assert isinstance(store, redis.StrictRedis)
    assert store.connection_pool.get_connection('').host == 'localhost'
    assert store.connection_pool.get_connection('').port == 6379
    assert store.connection_pool.get_connection('').db == db


def test_35_sentinel_connection(redis_client):
    with pytest.raises(ResponseError)  as exc_info:
        redis_client.execute_command('SELECT', 16)

    assert str(exc_info.value) == "DB index is out of range" 
    


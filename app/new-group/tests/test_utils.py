from new_group.utils import set_group_id
from _pytest.logging import LogCaptureFixture
from jc_redis.redis import RedisConnection
from unittest.mock import patch
from config.config import GROUPS_DB, GAKUNIN_GROUP_SUFFIX
from flask import Flask
import pytest
import logging
from logging import INFO
import subprocess
import redis

app = Flask(__name__)

def test_03_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            store.rpush(redis_key, "GakuNinTF")
            set_group_id("jc_test_org_groups_example")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == ["GakuNinTF", "jc_test_org_groups_example"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_groups_example) is set to Redis.') in info_logs

            
def test_04_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            store.rpush(redis_key, "GakuNinTF")
            store.rpush(redis_key, "jc_test_org_groups_example")
            set_group_id("jc_test_org_groups_example")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == ["GakuNinTF", "jc_test_org_groups_example"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_groups_example) is set to Redis.') in info_logs


def test_05_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            # binary_groups = store.lrange(redis_key, 0, -1)
            # str_groups = [str(group, 'utf-8') for group in binary_groups]
            # print('str_groupsの確認前', str_groups)
            set_group_id("jc_test_org_groups_example")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == ["jc_test_org_groups_example"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_groups_example) is set to Redis.') in info_logs


def test_06_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data_2):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            print('str_groupsの確認前', str_groups)
            set_group_id("jc_test_org_groups_example")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_groups_example) is not set to Redis.') in info_logs


def test_07_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            store.rpush(redis_key, "GakuNinTF")
            set_group_id("jc_test_org_roles_contributor")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == ["GakuNinTF", "jc_test_org_roles_contributor"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_roles_contributor) is set to Redis.') in info_logs


def test_08_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            store.rpush(redis_key, "GakuNinTF")
            store.rpush(redis_key, "jc_test_org_roles_contributor")
            set_group_id("jc_test_org_roles_contributor")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == ["GakuNinTF", "jc_test_org_roles_contributor"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_roles_contributor) is set to Redis.') in info_logs


def test_09_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("jc_test_org_roles_contributor")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == ["jc_test_org_roles_contributor"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_roles_contributor) is set to Redis.') in info_logs


def test_10_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data_2):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("jc_test_org_roles_contributor")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_roles_contributor) is not set to Redis.') in info_logs


def test_11_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            store.rpush(redis_key, "GakuNinTF")
            set_group_id("jc_test_org_groups")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == ["GakuNinTF"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_groups) is not set to Redis.') in info_logs


def test_12_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("jc_test_org_groups")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_groups) is not set to Redis.') in info_logs


def test_13_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data_2):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("jc_test_org_groups")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_groups) is not set to Redis.') in info_logs


def test_14_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            store.rpush(redis_key, "GakuNinTF")
            set_group_id("jc_test_org_roles")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        print('str_groupsの確認', str_groups)
        assert str_groups == ["GakuNinTF"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_roles) is not set to Redis.') in info_logs


def test_15_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("jc_test_org_roles")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_roles) is not set to Redis.') in info_logs


def test_16_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data_2):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("jc_test_org_roles")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(jc_test_org_roles) is not set to Redis.') in info_logs


def test_17_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            store.rpush(redis_key, "GakuNinTF")
            set_group_id("test_org_groups_example")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == ["GakuNinTF"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(test_org_groups_example) is not set to Redis.') in info_logs


def test_18_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("test_org_groups_example")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(test_org_groups_example) is not set to Redis.') in info_logs


def test_19_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data_2):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("test_org_groups_example")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(test_org_groups_example) is not set to Redis.') in info_logs


def test_20_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            store.rpush(redis_key, "GakuNinTF")
            set_group_id("test_org_roles_contributor")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == ["GakuNinTF"]
        assert ('tests.test_utils', logging.INFO, 'Group ID(test_org_roles_contributor) is not set to Redis.') in info_logs


def test_21_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("test_org_roles_contributor")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(test_org_roles_contributor) is not set to Redis.') in info_logs


def test_22_set_group_id(caplog: LogCaptureFixture):
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data_2):
            caplog.set_level(INFO)
            redis_connection = RedisConnection()
            store = redis_connection.connection(GROUPS_DB)
            redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
            store.flushdb()
            set_group_id("test_org_roles_contributor")
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            info_logs = [record for record in caplog.record_tuples if record[1] == logging.INFO]
        assert str_groups == []
        assert ('tests.test_utils', logging.INFO, 'Group ID(test_org_roles_contributor) is not set to Redis.') in info_logs


def test_23_set_group_id():
    with app.app_context():
        with patch('new_group.utils.set_group_id', side_effect=redis.ConnectionError):
            set_group_id("jc_test_org_groups_example")
        # with pytest.raises(ConnectionRefusedError) as excinfo:
            # redis_connection = RedisConnection()
            # store = redis_connection.connection(GROUPS_DB)
            # # store = redis.StrictRedis(host='localhost', port=6379, db=0)
            # store.shutdown()
            
        # assert "ConnectionError" in str(excinfo.value)

        # subprocess.run(["sudo", "systemctl", "restart", "redis"])


data = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/root/server.cer',
        'org_sp_fqdn': 'test.org'
    }
}

data_2 = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/root/server.cer',
        'org_sp_fqdn': 'xxxx'
    }
}
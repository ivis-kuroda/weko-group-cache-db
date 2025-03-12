import subprocess
from logging import INFO
from unittest.mock import patch

import pytest
from redis import ConnectionError

from config.config import GAKUNIN_GROUP_SUFFIX
from new_group.utils import set_group_id

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_03_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The value "jc_test_org_groups_example" is appended to the end of the key "test_org_gakunin_groups".
# "Group ID(jc_test_org_groups_example) is set to Redis." is logged.
def test_03_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.rpush(redis_key, "GakuNinTF")

        target_group_id = "jc_test_org_groups_example"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == ["GakuNinTF", target_group_id]
        assert 'Group ID({}) is set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_04_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The value "jc_test_org_groups_example" is not appended to the end of the key "test_org_gakunin_groups".
# "Group ID(jc_test_org_groups_example) is set to Redis." is logged.            
def test_04_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.rpush(redis_key, "GakuNinTF")
        prepare_redis_connection.rpush(redis_key, "jc_test_org_groups_example")

        target_group_id = "jc_test_org_groups_example"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == ["GakuNinTF", target_group_id]
        assert 'Group ID({}) is set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_05_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is created, and the value "jc_test_org_groups_example" is registered.
# "Group ID(jc_test_org_groups_example) is set to Redis." is logged.
def test_05_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "jc_test_org_groups_example"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == [target_group_id]
        assert 'Group ID({}) is set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_06_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created, and the value "jc_test_org_groups_example" is not registered.
# "Group ID(jc_test_org_groups_example) is not set to Redis." is logged.
def test_06_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    prepare_authorization_dict['Organization Name']['org_sp_fqdn'] = 'xxxx'
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.flushdb()

        target_group_id = "jc_test_org_groups_example"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_07_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The value "jc_test_org_roles_contributor" is appended to the end of the key "test_org_gakunin_groups".
# "Group ID(jc_test_org_roles_contributor) is set to Redis." is logged.
def test_07_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.rpush(redis_key, "GakuNinTF")

        target_group_id = "jc_test_org_roles_contributor"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == ["GakuNinTF", target_group_id]
        assert 'Group ID({}) is set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_08_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The value "jc_test_org_roles_contributor" is not appended to the end of the key "test_org_gakunin_groups".
# "Group ID(jc_test_org_roles_contributor) is set to Redis." is logged.
def test_08_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.rpush(redis_key, "GakuNinTF")
        prepare_redis_connection.rpush(redis_key, "jc_test_org_roles_contributor")

        target_group_id = "jc_test_org_roles_contributor"
        set_group_id(target_group_id)
        set_group_id("jc_test_org_roles_contributor")

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == ["GakuNinTF", target_group_id]
        assert 'Group ID({}) is set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_09_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is created, and the value "jc_test_org_roles_contributor" is registered.
# "Group ID(jc_test_org_roles_contributor) is set to Redis." is logged.
def test_09_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "jc_test_org_roles_contributor"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == [target_group_id]
        assert 'Group ID({}) is set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_10_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created, and the value "jc_test_org_roles_contributor" is not registered.
# "Group ID(jc_test_org_roles_contributor) is set to Redis." is logged.
def test_10_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    prepare_authorization_dict['Organization Name']['org_sp_fqdn'] = 'xxxx'
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "jc_test_org_roles_contributor"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_11_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The value "jc_test_org_groups" is not appended to the end of the key "test_org_gakunin_groups".
# "Group ID(jc_test_org_groups) is not set to Redis." is logged.
def test_11_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.rpush(redis_key, "GakuNinTF")

        target_group_id = "jc_test_org_groups"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == ["GakuNinTF"]
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_12_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created.
# "Group ID(jc_test_org_groups) is not set to Redis." is logged.
def test_12_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "jc_test_org_groups"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_13_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created.
# "Group ID(jc_test_org_groups) is not set to Redis." is logged.
def test_13_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    prepare_authorization_dict['Organization Name']['org_sp_fqdn'] = 'xxxx'
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "jc_test_org_groups"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_14_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The value "jc_test_org_roles" is not appended to the end of the key "test_org_gakunin_groups".
# "Group ID(jc_test_org_roles) is not set to Redis." is logged.
def test_14_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.rpush(redis_key, "GakuNinTF")

        target_group_id = "jc_test_org_roles"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == ["GakuNinTF"]
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_15_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created.
# "Group ID(jc_test_org_roles) is not set to Redis." is logged.
def test_15_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "jc_test_org_roles"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_16_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created.
# "Group ID(jc_test_org_roles) is not set to Redis." is logged.
def test_16_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    prepare_authorization_dict['Organization Name']['org_sp_fqdn'] = 'xxxx'
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "jc_test_org_roles"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_17_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The value "test_org_groups_example" is not appended to the end of the key "test_org_gakunin_groups".
# "Group ID(test_org_groups_example) is not set to Redis." is logged.
def test_17_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.rpush(redis_key, "GakuNinTF")

        target_group_id = "test_org_groups_example"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == ["GakuNinTF"]
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_18_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created.
# "Group ID(test_org_groups_example) is not set to Redis." is logged.
def test_18_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "test_org_groups_example"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_19_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created.
# "Group ID(test_org_groups_example) is not set to Redis." is logged.
def test_19_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    prepare_authorization_dict['Organization Name']['org_sp_fqdn'] = 'xxxx'
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "test_org_groups_example"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_20_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The value "test_org_roles_contributor" is not appended to the end of the key "test_org_gakunin_groups".
# "Group ID(test_org_roles_contributor) is not set to Redis." is logged.
def test_20_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX
        prepare_redis_connection.rpush(redis_key, "GakuNinTF")

        target_group_id = "test_org_roles_contributor"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == ["GakuNinTF"]
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_21_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created.
# "Group ID(test_org_roles_contributor) is not set to Redis." is logged.
def test_21_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "test_org_roles_contributor"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID({}) is not set to Redis.'.format(target_group_id) == info_logs[0]

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_22_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The key "test_org_gakunin_groups" is not created.
# "Group ID(test_org_roles_contributor) is not set to Redis." is logged.
def test_22_set_group_id(app, test_logger, prepare_authorization_dict, prepare_redis_connection):
    prepare_authorization_dict['Organization Name']['org_sp_fqdn'] = 'xxxx'
    with patch("config.config.SP_AUTHORIZATION_DICT", prepare_authorization_dict):
        redis_key = 'test_org' + GAKUNIN_GROUP_SUFFIX

        target_group_id = "test_org_roles_contributor"
        set_group_id(target_group_id)

        binary_groups = prepare_redis_connection.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]
        info_logs = [record[2] for record in test_logger.record_tuples if record[1] == INFO]
        assert str_groups == []
        assert 'Group ID(test_org_roles_contributor) is not set to Redis.' in info_logs

# def set_group_id(group_id):
# .tox/c1/bin/pytest --cov=new_group tests/test_utils.py::test_23_set_group_id -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# The connection to Redis is refused.
# ConnectionError is raised.
def test_23_set_group_id(app):
    subprocess.run(['docker', 'compose', 'stop', 'redis'])
    with pytest.raises(ConnectionError) as excinfo:
        set_group_id("jc_test_org_groups_example")

    assert 'Connection refused.' in str(excinfo.value)
    subprocess.run(['docker', 'compose', 'start', 'redis'])

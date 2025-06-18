from unittest.mock import MagicMock, patch

import pytest
from requests import Response

from config.config import GAKUNIN_GROUP_SUFFIX, GROUPS_DB
from jc_redis.redis_conn import RedisConnection
from get_groups.utils import get_groups_from_gakunin, set_groups, set_groups_to_redis

# def set_groups(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_11_set_groups -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Process completed successfully
def test_11_set_groups(prepare_authorization_dict):
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

            try:
                set_groups('org.sp.co.jp')
            except Exception:
                assert False

# def set_groups(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_12_set_groups -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# Process completed successfully
def test_12_set_groups(prepare_authorization_dict):
    key_name = 'Organization Name'
    prepare_authorization_dict[key_name]['org_sp_fqdn'] = 'org_sp_co.jp'
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
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

            try:
                set_groups('org_sp_co.jp')
            except Exception:
                assert False

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_13_get_groups_from_gakunin -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# retrieved group information is returned
def test_13_get_groups_from_gakunin(prepare_authorization_dict):
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
            result = get_groups_from_gakunin('org.sp.co.jp')
        
            assert [{"id" : "https://cg.gakunin.jp/gr/GakuNinTF","title" : "group","description" : "group-test","map_totalMembers" : 1}] == result

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_14_get_groups_from_gakunin -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "FQDN([fqdn]) is not found in config." exception
def test_14_get_groups_from_gakunin(prepare_authorization_dict):
    with patch('config.config.SP_AUTHORIZATION_DICT', prepare_authorization_dict):
        target_fqdn = 'XXXXXXX'
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin(target_fqdn)

        assert str(excinfo.value) == "FQDN({}) is not found in config.".format(target_fqdn)

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_15_get_groups_from_gakunin -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "FQDN(sp_connector_id is not found in config for FQDN([fqdn])." exception
def test_15_get_groups_from_gakunin(prepare_authorization_dict):
    key_name = 'Organization Name'
    prepare_authorization_dict[key_name].pop('sp_connector_id')
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
        target_fqdn = 'org.sp.co.jp'
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin(target_fqdn)

        assert str(excinfo.value) == "sp_connector_id is not found in config for FQDN({}).".format(target_fqdn)

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_16_get_groups_from_gakunin -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "FQDN(sp_connector_id is not found in config for FQDN([fqdn])." exception
def test_16_get_groups_from_gakunin(prepare_authorization_dict):
    key_name = 'Organization Name'
    prepare_authorization_dict[key_name]['sp_connector_id'] = ''
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
        target_fqdn = 'org.sp.co.jp'
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin(target_fqdn)

        assert str(excinfo.value) == "sp_connector_id is not found in config for FQDN({}).".format(target_fqdn)

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_17_get_groups_from_gakunin -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "FQDN(tls_client_cert is not found in config for FQDN([fqdn])." exception
def test_17_get_groups_from_gakunin(prepare_authorization_dict):
    key_name = 'Organization Name'
    prepare_authorization_dict[key_name].pop('tls_client_cert')
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
        target_fqdn = 'org.sp.co.jp'
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin(target_fqdn)

        assert str(excinfo.value) == "tls_client_cert is not found in config for FQDN({}).".format(target_fqdn)

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_18_get_groups_from_gakunin -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "FQDN(tls_client_cert is not found in config for FQDN([fqdn])." exception
def test_18_get_groups_from_gakunin(prepare_authorization_dict):
    key_name = 'Organization Name'
    prepare_authorization_dict[key_name]['tls_client_cert'] = ''
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
        target_fqdn = 'org.sp.co.jp'
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin(target_fqdn)

        assert str(excinfo.value) == "tls_client_cert is not found in config for FQDN({}).".format(target_fqdn)

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_19_get_groups_from_gakunin -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# "FQDN(tls_client_cert([tls_client_cert]) is not found." exception
def test_19_get_groups_from_gakunin(prepare_authorization_dict):
    key_name = 'Organization Name'
    prepare_authorization_dict[key_name]['tls_client_cert'] = '/XXX/YYY.cer'
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
        target_fqdn = 'org.sp.co.jp'
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin(target_fqdn)

        assert str(excinfo.value) == "tls_client_cert({}) is not found.".format('/XXX/YYY.cer')

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_get_groups_from_gakunin_key_file -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
def test_get_groups_from_gakunin_key_file(prepare_authorization_dict):
    key_name = 'Organization Name'
    prepare_authorization_dict[key_name]['tls_client_key'] = ''
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
        target_fqdn = 'org.sp.co.jp'
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin(target_fqdn)

        assert str(excinfo.value) == "tls_client_key is not found in config for FQDN({}).".format(target_fqdn)
    
    prepare_authorization_dict[key_name]['tls_client_key'] = '/XXX/YYY.key'
    mock_data = {
        key_name: prepare_authorization_dict[key_name]
    }
    with patch('config.config.SP_AUTHORIZATION_DICT', mock_data):
        target_fqdn = 'org.sp.co.jp'
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin(target_fqdn)

        assert str(excinfo.value) == "tls_client_key({}) is not found.".format('/XXX/YYY.key')

# def get_groups_from_gakunin(fqdn):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_20_get_groups_from_gakunin -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# 404 Client Error
def test_20_get_groups_from_gakunin(prepare_authorization_dict):
    with patch('config.config.SP_AUTHORIZATION_DICT', prepare_authorization_dict):
        with patch('requests.get') as mock_get:
            mock_response = Response()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            with pytest.raises(Exception) as excinfo:
                get_groups_from_gakunin('org.sp.co.jp')

            assert '404 Client Error' in str(excinfo.value)

# def set_groups_to_redis(fqdn, group_id_list):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_21_set_groups_to_redis -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# [fqdn]_gakunin_groups should be registered in the key of Redis.
# The specified group_id_list must be registered as the value of the key with the list type.
# The expiration date of the key must be set to 86400.
def test_21_set_groups_to_redis():
    with patch('config.config.GROUPS_TTL', 86400):
        redis_connection = RedisConnection()
        store = redis_connection.connection(GROUPS_DB)
        store.flushdb()
        target_fqdn = 'org_sp_co_jp'
        set_groups_to_redis(target_fqdn, ["GakuNinTF"])
        redis_key = target_fqdn + GAKUNIN_GROUP_SUFFIX
        binary_groups = store.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]

        assert str_groups == ["GakuNinTF"]
        assert 86398 <= store.ttl(redis_key) <= 86400

# def set_groups_to_redis(fqdn, group_id_list):
# .tox/c1/bin/pytest --cov=get_groups tests/test_utils.py::test_22_set_groups_to_redis -s -vv -s --cov-branch --cov-report=term --basetemp=.tox/c1/tmp
# [fqdn]_gakunin_groups should be registered in the key of Redis.
# Only the value of group_id_list specified for the key value should be registered with the list type.
# The expiration date of the key must be set to 86400.
def test_22_set_groups_to_redis():
    with patch('config.config.GROUPS_TTL', 86400):
        redis_connection = RedisConnection()
        store = redis_connection.connection(GROUPS_DB)
        target_fqdn = 'org_sp_co_jp'
        redis_key = target_fqdn + GAKUNIN_GROUP_SUFFIX
        store.rpush(redis_key, "GakuNinTF")
        set_groups_to_redis(target_fqdn, ["AAAAA"])
        binary_groups = store.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]

        assert str_groups == ["AAAAA"]
        assert 86398 <= store.ttl(redis_key) <= 86400

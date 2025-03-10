import pytest
from jc_redis.redis import RedisConnection
from get_groups.utils import set_groups, get_groups_from_gakunin, set_groups_to_redis
from config.config import GROUPS_DB, GAKUNIN_GROUP_SUFFIX
from unittest.mock import patch, MagicMock


def test_11_set_groups():
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
            try:
                set_groups('org.idp.co,jp')
            except Exception:
                assert False


def test_12_set_groups():
    with patch('config.config.SP_AUTHORIZATION_DICT', data_2):
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
            try:
                set_groups('org_idp_co,jp')
            except Exception:
                assert False


def test_13_get_groups_from_gakunin():
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
            result = get_groups_from_gakunin('org.idp.co,jp')
        
        assert [{"id" : "https:\/\/cg.gakunin.jp\/gr\/GakuNinTF","title" : "group","description" : "group-test","map_totalMembers" : 1}] == result


def test_14_get_groups_from_gakunin():
    with patch('config.config.SP_AUTHORIZATION_DICT', data_14):
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin('XXXXXXX')

        assert str(excinfo.value) == "FQDN(XXXXXXX) is not found in config.".format('XXXXXXX')


def test_15_get_groups_from_gakunin():
    with patch('config.config.SP_AUTHORIZATION_DICT', data_15):
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin('org.idp.co,jp')

        assert str(excinfo.value) == "sp_connector_id is not found in config for FQDN({}).".format('org.idp.co,jp')


def test_16_get_groups_from_gakunin():
    with patch('config.config.SP_AUTHORIZATION_DICT', data_16):
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin('org.idp.co,jp')

        assert str(excinfo.value) == "sp_connector_id is not found in config for FQDN({}).".format('org.idp.co,jp')


def test_17_get_groups_from_gakunin():
    with patch('config.config.SP_AUTHORIZATION_DICT', data_17):
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin('org.idp.co,jp')

        assert str(excinfo.value) == "tls_client_cert is not found in config for FQDN({}).".format('org.idp.co,jp')


def test_18_get_groups_from_gakunin():
    with patch('config.config.SP_AUTHORIZATION_DICT', data_18):
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin('org.idp.co,jp')

        assert str(excinfo.value) == "tls_client_cert is not found in config for FQDN({}).".format('org.idp.co,jp')


def test_19_get_groups_from_gakunin():
    with patch('config.config.SP_AUTHORIZATION_DICT', data_19):
        with pytest.raises(Exception) as excinfo:
            get_groups_from_gakunin('org.idp.co,jp')

        assert str(excinfo.value) == "tls_client_cert({}) is not found.".format('/XXX/YYY.cer')


def test_20_get_groups_from_gakunin():
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        with patch('config.config.GROUPS_API_URL', 'http://localhost/test/grapes/'):
            with pytest.raises(Exception) as excinfo:
                get_groups_from_gakunin('org.idp.co,jp')

            assert '404 Client Error' in str(excinfo.value)


def test_21_set_groups_to_redis():
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        redis_connection = RedisConnection()
        store = redis_connection.connection(GROUPS_DB)
        store.flushdb()
        set_groups_to_redis('org.idp.co,jp', ["GakuNinTF"])
        redis_key = 'org.idp.co,jp' + GAKUNIN_GROUP_SUFFIX
        binary_groups = store.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]

    assert str_groups == ["GakuNinTF"]
    assert 86398 <= store.ttl(redis_key) <= 86400


def test_22_set_groups_to_redis():
    with patch('config.config.SP_AUTHORIZATION_DICT', data):
        redis_connection = RedisConnection()
        store = redis_connection.connection(GROUPS_DB)
        redis_key = 'org.idp.co,jp' + GAKUNIN_GROUP_SUFFIX
        store.rpush(redis_key, "GakuNinTF")
        set_groups_to_redis('org.idp.co,jp', ["AAAAA"])
        binary_groups = store.lrange(redis_key, 0, -1)
        str_groups = [str(group, 'utf-8') for group in binary_groups]

    assert str_groups == ["AAAAA"]
    assert 86398 <= store.ttl(redis_key) <= 86400


data = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}

data_2 = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org_idp_co,jp'
    },
}

data_14 = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}

data_15 = {
    'Organization Name': {
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}

data_16 = {
    'Organization Name': {
        'sp_connector_id': '',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}

data_17 = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}

data_18 = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}

data_19 = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/XXX/YYY.cer',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}

data_21 = {
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
    'Organization Name': {
        'sp_connector_id': 'connector1',
        'tls_client_cert': '/etc/nginx/cert/server.crt',
        'org_sp_fqdn': 'org.idp.co,jp'
    },
}

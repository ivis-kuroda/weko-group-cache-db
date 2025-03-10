from new_group.api import set_new_group_id
from unittest.mock import patch
from flask import Flask
import pytest
from unittest.mock import MagicMock
from unittest.mock import Mock


app = Flask(__name__)

def test_01_set_new_group_id():
    with app.app_context():
        with patch("config.config.SP_AUTHORIZATION_DICT", data):
            result = set_new_group_id('jc_test_org_groups_example')
        assert result.json == {"result": "OK","message": "Success."}


def test_02_set_new_group_id():
    with app.app_context():
        with patch("new_group.utils.set_group_id", side_effect=ValueError("Test Exception occurred.")) as ex:
            
            set_group_id = MagicMock(side_effect=ValueError("Test Exception occurred."))
            
            # with pytest.raises(Exception) as ex:
            
            ex.side_effect = ValueError("Test Exception occurred.")
            result = set_new_group_id('jc_test_org_groups_example')
            print('result:', result.json)
            
            assert result.json == {"result": "NG","message": str({}).format(ex)}


def test_02_2_set_new_group_id():
    with app.app_context():
        with patch('new_group.api.set_group_id', side_effect=Exception("Test Exception occurred.")):
            result = set_new_group_id('jc_test_org_groups_example')
            assert result.json == {"result": "NG", "message": 'Test Exception occurred.'}


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
        'org_sp_fqdn': 'test'
    }
}
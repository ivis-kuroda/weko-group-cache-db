import os
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests

from config import config, messages
from jc_redis.redis_conn import RedisConnection

def set_groups(fqdn):
    """Get groups from Gakunin API and set to Redis
    
    Arguments:
        fqdn(str): fqdn of the target sp
    """
    # get group_id_list from gakunin
    groups = get_groups_from_gakunin(fqdn)
    group_id_list = []
    for group in groups:
        group_id = group['id'].split('/')[-1]
        group_id_list.append(group_id)

    # replace special characters
    fqdn = fqdn.replace('.', '_').replace('-', '_')

    # set groups to redis
    set_groups_to_redis(fqdn, group_id_list)

def get_groups_from_gakunin(fqdn):
    """Get groups from Gakunin API
    
    Arguments:
        fqdn(str): fqdn of the target sp
        
    Returns:
        list: list of groups
    """
    target_sp = None
    # get sp connection details
    for value in config.SP_AUTHORIZATION_DICT.values():
        if value['org_sp_fqdn'] == fqdn:
            target_sp = value
            break
    if not target_sp:
        raise Exception(messages.FQDN_NOT_FOUND.format(fqdn))
    if not target_sp.get('sp_connector_id'):
        raise Exception(messages.SP_CONNECTOR_ID_NOT_FOUND.format(fqdn))
    if not target_sp.get('tls_client_cert'):
        raise Exception(messages.TLS_CLIENT_CERT_NOT_FOUND.format(fqdn))
    if not os.path.exists(target_sp['tls_client_cert']):
        raise Exception(messages.TLS_CLIENT_CERT_FILE_NOT_FOUND.format(target_sp['tls_client_cert']))
    if not target_sp.get('tls_client_key'):
        raise Exception(messages.TLS_CLIENT_KEY_NOT_FOUND.format(fqdn))
    if not os.path.exists(target_sp['tls_client_key']):
        raise Exception(messages.TLS_CLIENT_KEY_FILE_NOT_FOUND.format(target_sp['tls_client_key']))
    target_url = urljoin(config.GROUPS_API_URL, target_sp['sp_connector_id'])
    # get groups what connected to the target sp
    response = requests.get(target_url, cert=(target_sp['tls_client_cert'], target_sp['tls_client_key']))
    response.raise_for_status()
    return response.json()['entry']

def set_groups_to_redis(fqdn, group_id_list):
    """Set groups to redis
    
    Arguments:
        fqdn(str): fqdn of the target sp
        group_id_list(list): list of group ids
    """
    # get redis connection
    redis_connection = RedisConnection()
    store = redis_connection.connection(config.GROUPS_DB)
    # create redis key
    redis_key = fqdn + config.GAKUNIN_GROUP_SUFFIX
    # set new group list and expire time
    updated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    store.hset(redis_key, mapping={"updated_at": updated_at, "groups": ",".join(group_id_list)})
    store.expire(redis_key, config.GROUPS_TTL)

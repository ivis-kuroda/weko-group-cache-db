from flask import current_app

from config import config, messages
from jc_redis.redis import RedisConnection

def set_group_id(group_id):
    """Set group id to Redis

    Arguments:
        group_id(str): Group id
    """
    try:
        special_chars = config.GROUP_ID_SPECIAL_CHARS
        redis_connection = RedisConnection()
        store = redis_connection.connection(config.GROUPS_DB)
        if group_id.startswith(special_chars['prefix'])\
            and (special_chars['group_suffix'] in group_id or special_chars['role_suffix'] in group_id):
            # Register the group ID that follows the format
            if special_chars['group_suffix'] in group_id:
                idx = group_id.index(special_chars['group_suffix'])
                fqdn = group_id[len(special_chars['prefix']):idx]
            else:
                idx = group_id.index(special_chars['role_suffix'])
                fqdn = group_id[len(special_chars['prefix']):idx]
            redis_key = fqdn + config.GAKUNIN_GROUP_SUFFIX
            binary_groups = store.lrange(redis_key, 0, -1)
            str_groups = [str(group, 'utf-8') for group in binary_groups]
            if str_groups:
                if group_id not in str_groups:
                    # Register the group ID that does not exist in the Redis
                    store.rpush(redis_key, group_id)
            else:
                fqdn_list = [info['org_sp_fqdn'].replace('.', '_').replace('-', '_')
                             for info in config.SP_AUTHORIZATION_DICT.values()]
                if fqdn in fqdn_list:
                    # Register the group ID that fqdn is in the SP_AUTHORIZATION_DICT
                    store.rpush(redis_key, group_id)
            current_app.logger.info(messages.GROUP_ID_SET.format(group_id))
        else:
            # Not register the group ID that does not follow the format
            current_app.logger.info(messages.GROUP_ID_NOT_SET.format(group_id))
    except Exception as ex:
        raise ex

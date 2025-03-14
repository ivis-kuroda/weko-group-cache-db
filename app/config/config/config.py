# sp authorization information for getting groups
#   sp_connector_id: sp connector id
#   tls_client_cert: path to tls client certification
#   org_sp_fqdn: fqdn of SP 
SP_AUTHORIZATION_DICT = {
}

# special characters what are used in group_id
#   prefix: prefix of group_id
#   group_suffix: suffix of group_id for groups
#   role_suffix: suffix of group_id for roles
#   sys_admin_group: system admin group id
GROUP_ID_SPECIAL_CHARS = {
    'prefix': 'jc_',
    'group_suffix': '_groups_',
    'role_suffix': '_roles_',
    'sys_admin_group': 'jc_roles_sys'
}

# suffix of redis key for gakunin groups
GAKUNIN_GROUP_SUFFIX = '_gakunin_groups'

# Gakunin API URL(Groups API)
GROUPS_API_URL = 'https://cg.gakunin.jp/api/groups/'

# redis config
CACHE_TYPE = 'redis'
REDIS_HOST = 'redis'
REDIS_URL = 'redis://' + REDIS_HOST + ':6379/'
GROUPS_DB = 0
CELERY_BROKER_DB = 1
CELERY_BACKEND_DB = 2
GROUPS_TTL = 86400
CACHE_REDIS_SENTINEL_MASTER = 'mymaster'
CACHE_REDIS_SENTINELS = [("sentinel-service.re","26379")]

# logging config
CLI_LOG_LEVEL = 'INFO'
CLI_LOG_OUTPUT_PATH = '/var/log/cache-db/cli.log'

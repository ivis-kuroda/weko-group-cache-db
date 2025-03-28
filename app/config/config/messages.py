# app/get-groups/get_groups/cli.py
COMMAND_SUCCESS = '{} is success.'
COMMAND_FAILED = '{} is failed: {}'
COMMAND_FAILED_DETAIL = 'For details, see {}.'

# app/get-groups/get_groups/tasks.py
CREATE_TASK_SUCCESS = 'All set_groups_task are created.'
CREATE_TASK_FAILED = 'Error occurred in create_set_groups_task.'
FQDN_NOT_DEFINED = 'FQDN is not defined in config for {}.'
TASK_SUCCESS = 'FQDN({}) is success.'
TASK_FAILED = 'FQDN({}) is failed.'

# app/get-groups/get_groups/utils.py
FQDN_NOT_FOUND = 'FQDN({}) is not found in config.'
SP_CONNECTOR_ID_NOT_FOUND = 'sp_connector_id is not found in config for FQDN({}).'
TLS_CLIENT_CERT_NOT_FOUND = 'tls_client_cert is not found in config for FQDN({}).'
TLS_CLIENT_CERT_FILE_NOT_FOUND = 'tls_client_cert({}) is not found.'

# app/new-group/new_group/utils.py
GROUP_ID_SET = 'Group ID({}) is set to Redis.'
GROUP_ID_NOT_SET = 'Group ID({}) is not set to Redis.'
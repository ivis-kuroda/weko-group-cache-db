import logging

from . import config
from . import messages
from .utils import set_groups

logger = logging.getLogger(__name__)

def create_set_groups_task():
    """Create set_groups_task for all sp in config.
    """
    # get all sp info what is defined in config
    org_list = config.SP_AUTHORIZATION_DICT.keys()

    try:
        for org in org_list:
            if not config.SP_AUTHORIZATION_DICT[org].get('org_sp_fqdn'):
                logger.error(messages.FQDN_NOT_DEFINED.format(org))
                continue
            set_groups_task(config.SP_AUTHORIZATION_DICT[org]['org_sp_fqdn'])
    except Exception as ex:
        logger.error(messages.CREATE_TASK_FAILED, exc_info=True)
        raise ex
    logger.info(messages.CREATE_TASK_SUCCESS)

def set_groups_task(fqdn):
    """Get groups from Gakunin API and set to Redis

    Arguments:
        fqdn(str): fqdn of the target sp
    """
    try:
        set_groups(fqdn)
        logger.info(messages.TASK_SUCCESS.format(fqdn))
    except Exception as ex:
        logger.error(messages.TASK_FAILED.format(fqdn), exc_info=True)
        raise ex

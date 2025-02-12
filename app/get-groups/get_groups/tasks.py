from celery import shared_task
from celery.utils.log import get_task_logger

from config import config, messages
from .utils import set_groups

logger = get_task_logger(__name__)

@shared_task
def create_set_groups_task():
    """Create set_groups_task for all sp in config.
    """
    # get all sp info what is defined in config
    org_list = config.SP_AUTHORIZATION_DICT.keys()

    try:
        for org in org_list:
            set_groups_task.delay(org['org_sp_fqdn'])
    except Exception as ex:
        logger.error(messages.CREATE_TASK_FAILED, exc_info=True)
        raise ex
    logger.info(messages.CREATE_TASK_SUCCESS)

@shared_task
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
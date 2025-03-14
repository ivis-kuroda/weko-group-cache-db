from logging import FileHandler, Formatter, getLogger

import click

from config import config, messages
from .utils import set_groups

logger = getLogger(__name__)
logger.setLevel(config.CLI_LOG_LEVEL)

file_handler = FileHandler(config.CLI_LOG_OUTPUT_PATH)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@click.group()
def group():
    """Group commands."""

@group.command()
@click.option('-f', '--fqdn', required=True)
def get_groups(fqdn):
    """Get groups from Gakunin API and set to Redis
    
    Arguments:
        fqdn(str): fqdn of the target sp
    """
    try:
        set_groups(fqdn)
        click.secho(messages.COMMAND_SUCCESS.format(fqdn), fg='green')
        logger.info(messages.COMMAND_SUCCESS.format(fqdn))
    except Exception as ex:
        click.secho(messages.COMMAND_FAILED.format(fqdn, ex), fg='red')
        click.secho(messages.COMMAND_FAILED_DETAIL.format(config.CLI_LOG_OUTPUT_PATH), fg='red')
        logger.error(ex, exc_info=True)

#
# Copyright (C) 2025 National Institute of Informatics.
#

"""CLI module for weko-group-cache-db."""

import click as click_
import rich_click as click

from .config import setup_config
from .logger import setup_logger
from .utils import fetch_all

click.rich_click.SHOW_ARGUMENTS = True


DEFAULT_CONFIG_PATH = "config.toml"
DEFAULT_INSTITUTIONS_PATH = "institutions.toml"


@click.group()
@click.rich_config({"theme": "nord-modern"})
def main():
    """Run the command line interface for weko-group-cache-db."""


@main.command(context_settings={"show_default": True})
@click.option(
    "--file-path",
    "-f",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    required=False,
    default=DEFAULT_INSTITUTIONS_PATH,
    help="Specify the path to the TOML file containing institution data.",
)
@click.option(
    "--config-path",
    "-c",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    required=False,
    default=DEFAULT_CONFIG_PATH,
    help="Specify the path to the configuration TOML file.",
)
def run(file_path: str, config_path: str):
    """Fetch and cache groups for all institutions.

    Raises:
        Exit: If fetching or caching fails even for one institution.

    """
    setup_config(config_path)
    setup_logger(__package__)  # pyright: ignore[reportArgumentType]
    code = fetch_all(file_path)

    if code != 0:
        raise click_.exceptions.Exit(code)

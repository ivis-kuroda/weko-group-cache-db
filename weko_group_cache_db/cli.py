#
# Copyright (C) 2025 National Institute of Informatics.
#

"""CLI module for weko-group-cache-db."""

import operator

import click as click_
import rich_click as click

from .config import setup_config
from .groups import fetch_all, fetch_one
from .logger import logger, setup_logger

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
    default=None,
    help="Specify the path to the TOML file containing institution data.",
)
@click.option(
    "--directory-path",
    "-d",
    type=click.Path(exists=True, file_okay=False, path_type=str),
    required=False,
    default=None,
    help="Specify the path to the directory containing TOML files.",
)
@click.option(
    "--fqdn-list-file",
    "-l",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    required=False,
    default=None,
    help="Specify the path to the file containing FQDN list.",
)
@click.option(
    "--config-path",
    "-c",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    required=False,
    default=DEFAULT_CONFIG_PATH,
    help="Specify the path to the configuration TOML file.",
)
def run(file_path: str, directory_path: str, fqdn_list_file: str, config_path: str):
    """Fetch and cache groups for all institutions.

    Cannot specify both --file-path and --directory-path/--fqdn-list-file.

    """
    setup_config(config_path)
    setup_logger(__package__)  # pyright: ignore[reportArgumentType]

    validate_source_options(file_path, directory_path, fqdn_list_file)

    if directory_path and fqdn_list_file:
        logger.info(
            f"Loading from directory source: {directory_path} and {fqdn_list_file}"
        )
        fetch_all(directory_path=directory_path, fqdn_list_file=fqdn_list_file)
    else:
        if file_path is None:
            file_path = DEFAULT_INSTITUTIONS_PATH

        logger.info(f"Loading from file source: {file_path}")
        fetch_all(toml_path=file_path)


@main.command(context_settings={"show_default": True})
@click.argument(
    "fqdn",
    type=str,
    required=True,
    nargs=1,
    metavar="FQDN",
    help="Specify the FQDN of the institution to fetch and cache groups for.",
)
@click.option(
    "--file-path",
    "-f",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    required=False,
    default=None,
    help="Specify the path to the TOML file containing institution data.",
)
@click.option(
    "--directory-path",
    "-d",
    type=click.Path(exists=True, file_okay=False, path_type=str),
    required=False,
    default=None,
    help="Specify the path to the directory containing TOML files.",
)
@click.option(
    "--fqdn-list-file",
    "-l",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    required=False,
    default=None,
    help="Specify the path to the file containing FQDN list.",
)
@click.option(
    "--config-path",
    "-c",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    required=False,
    default=DEFAULT_CONFIG_PATH,
    help="Specify the path to the configuration TOML file.",
)
def one(
    fqdn: str,
    file_path: str,
    directory_path: str,
    fqdn_list_file: str,
    config_path: str,
):
    """Fetch and cache groups for a single institution.

    Cannot specify both --file-path and --directory-path/--fqdn-list-file.

    """
    setup_config(config_path)
    setup_logger(__package__)  # pyright: ignore[reportArgumentType]

    validate_source_options(file_path, directory_path, fqdn_list_file)

    if directory_path and fqdn_list_file:
        logger.info(
            f"Loading from directory source: {directory_path} and {fqdn_list_file}"
        )
        fetch_one(fqdn, directory_path=directory_path, fqdn_list_file=fqdn_list_file)
    else:
        if file_path is None:
            file_path = DEFAULT_INSTITUTIONS_PATH

        logger.info(f"Loading from file source: {file_path}")
        fetch_one(fqdn, toml_path=file_path)


def validate_source_options(
    file_path: str | None,
    directory_path: str | None,
    fqdn_list_file: str | None,
) -> None:
    """Validate source options for loading institution information.

    Raises:
        click.UsageError: If the source options are invalid.

    """
    if file_path and (directory_path or fqdn_list_file):
        error = "Cannot specify both --file-path and --directory-path/--fqdn-list-file."
        raise click_.UsageError(error)

    if not file_path and operator.xor(directory_path is None, fqdn_list_file is None):
        error = "Both --directory-path and --fqdn-list-file must be specified."
        raise click_.UsageError(error)

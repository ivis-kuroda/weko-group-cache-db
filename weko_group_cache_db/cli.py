#
# Copyright (C) 2025 National Institute of Informatics.
#

"""CLI module for weko-group-cache-db."""

import click

from .logger import logger
from .utils import fetch_all


@click.group()
def main():
    """Run the command line interface for weko-group-cache-db."""
    logger.info("weko-group-cache-db CLI")


@main.command()
@click.option(
    "--file-path",
    "-f",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    required=False,
    default="institutions.toml",
    help="Specify the path to the TOML file containing institution data.",
)
def run(file_path: str):
    """Fetch and cache groups for all institutions."""
    fetch_all(file_path)

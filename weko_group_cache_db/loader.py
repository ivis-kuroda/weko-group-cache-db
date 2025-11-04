#
# Copyright (C) 2025 National Institute of Informatics.
#

"""File loader module for weko-group-cache-db."""

import tomllib

from pathlib import Path
from tomllib import TOMLDecodeError

import inflect

from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import ValidationError
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

from .logger import console, logger


def load_institutions(toml_path: str | Path) -> list[Institution]:
    """Load institution information from TOML file.

    Arguments:
        toml_path (Path): Path to the TOML file.

    Returns:
        list[Institution]: List of Institution objects.

    Raises:
        ValueError: If the TOML file cannot be read.
        TOMLDecodeError: If the TOML file is invalid.

    """
    if isinstance(toml_path, str):
        toml_path = Path(toml_path)

    with console.status("Loading institutions from TOML file"):
        try:
            with toml_path.open("rb") as f:
                toml_data = tomllib.load(f)
        except FileNotFoundError:
            logger.error("TOML file not found: %s", toml_path)
            return []
        except TOMLDecodeError, ValueError:
            logger.error("Failed to load TOML file: %s", toml_path)
            raise

        if "institutions" not in toml_data:
            logger.error("No 'institutions' section found in the TOML file.")
            return []

        if not isinstance(toml_data["institutions"], list):
            logger.error("Invalid 'institutions' section format in the TOML file.")
            return []

    p = inflect.engine()
    institutions: list[Institution] = []
    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            "Validating institution entries...", total=len(toml_data["institutions"])
        )
        for index, item in enumerate(toml_data["institutions"]):
            ordinal = p.ordinal(index + 1)  # pyright: ignore[reportArgumentType]

            try:
                institution = Institution.model_validate(item)
            except ValidationError:
                institution_fqdn = item.get("fqdn", "Unknown")
                progress.log(
                    f"Failed to load {ordinal} institution '{institution_fqdn}'.",
                )
                console.print_exception()
                continue
            else:
                if not check_existence_file(institution):
                    progress.log(
                        f"Skip {ordinal} institution '{institution.fqdn}' "
                        "due to missing TLS client cert/key files.",
                    )
                    continue

                institutions.append(institution)
            finally:
                progress.update(task, advance=1)

    logger.info("%d institutions loaded successfully.", len(institutions))

    return institutions


def check_existence_file(institution: Institution) -> bool:
    """Check existence of TLS client cert and key files.

    Arguments:
        institution (Institution): Institution object.
        ordinal (str | None): Ordinal representation of the institution index.

    Returns:
        bool: True if both files exist, False otherwise.

    """
    cert_path = Path(institution.client_cert_path)
    key_path = Path(institution.client_key_path)

    return cert_path.exists() and key_path.exists()


class Institution(BaseModel):
    """Institution model for loading from TOML file."""

    name: str | None
    """Name of the institution. Optional."""

    fqdn: str
    """FQDN of the institution."""

    sp_connector_id: str = Field(..., validation_alias="spid")
    """Service Provider Connector ID of the institution."""

    client_cert_path: str = Field(..., validation_alias="cert")
    """Path to TLS client certificate file."""

    client_key_path: str = Field(..., validation_alias="key")
    """Path to TLS client key file."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

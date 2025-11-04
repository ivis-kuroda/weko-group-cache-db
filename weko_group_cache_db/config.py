#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Settings module for weko-group-cache-db."""

import tomllib
import typing as t

from contextvars import ContextVar
from pathlib import Path

import rich_click as click

from pydantic import BaseModel, computed_field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from werkzeug.local import LocalProxy

if t.TYPE_CHECKING:
    from pydantic.fields import FieldInfo  # pragma: no cover


class Settings(BaseSettings):
    """Settings for application with validation."""

    DEVELOPMENT: bool = False
    """Environment flag for development."""

    LOG_LEVEL: t.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    """Logging level.

    Possible values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
    """

    CACHE_KEY_SUFFIX: str = "_gakunin_groups"
    """Cache key suffix of group information in Redis."""

    CACHE_TTL: t.Annotated[int, "seconds"] = 86400
    """Cache time-to-live of group information in Redis.

    If it specified less than 0, it will be considered as no expiration.
    """

    MAP_GROUPS_API_ENDPOINT: str
    """Map groups API endpoint."""

    REQUEST_TIMEOUT: t.Annotated[int, "seconds"] = 20
    """Request timeout when connecting to mAP API."""

    REQUEST_INTERVAL: t.Annotated[int, "seconds"] = 5
    """Request interval when fetching groups from mAP API."""

    REQUEST_RETRIES: t.Annotated[int, "times"] = 3
    """Request retries when failed to fetch groups from mAP API."""

    REDIS_TYPE: t.Literal["redis", "sentinel"] = "redis"
    """Redis type to use. `redis` or `sentinel` is allowed."""

    REDIS_HOST: str = "localhost"
    """Redis service host name."""

    REDIS_PORT: int = 6379
    """Redis service port number."""

    REDIS_DB_INDEX: int = 4
    """Redis DB index to use for caching group information."""

    @computed_field
    @property
    def REDIS_URL(self) -> str:  # noqa: N802
        """Redis URL for caching group information."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_INDEX}"

    REDIS_SENTINEL_MASTER: str | None = None
    """Server name of the Redis sentinel master."""

    SENTINELS: list[Sentinel] | None = None
    """A list of Redis sentinel configurations."""

    @computed_field
    @property
    def REDIS_SENTINELS(self) -> list[tuple[str, str]]:  # noqa: N802
        """A list of Redis sentinel host names and their ports."""
        return (
            [(sentinel.host, str(sentinel.port)) for sentinel in self.SENTINELS]
            if self.SENTINELS
            else []
        )

    model_config = SettingsConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
    )

    toml_path: Path | None = None
    """Path to the TOML configuration file."""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize settings sources.

        Returns:
            A tuple of customized settings sources sorted by priority.

        """
        toml_path: str | Path | None = init_settings().get("toml_path")

        if toml_path is None:
            return super().settings_customise_sources(
                settings_cls,
                init_settings,
                env_settings,
                dotenv_settings,
                file_secret_settings,
            )

        if isinstance(toml_path, str):
            toml_path = Path(toml_path)
        toml_settings = TomlConfigSettingsSource(cls, toml_path)

        return (
            init_settings,
            toml_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


class Sentinel(BaseModel):
    """Redis sentinel configuration."""

    host: str
    """Sentinel host name."""

    port: int
    """Sentinel port number."""


class TomlConfigSettingsSource(PydanticBaseSettingsSource):
    """TOML configuration settings source."""

    def __init__(self, settings_cls: type[BaseSettings], toml_path: Path) -> None:
        """Initialize TOML config settings source."""
        super().__init__(settings_cls)
        self.toml_path = toml_path

    def get_field_value(
        self,
        field: FieldInfo,  # noqa: ARG002
        field_name: str,
    ) -> tuple[t.Any, str, bool]:
        """Get the value of a field from the TOML file."""  # noqa: DOC201
        data = getattr(self, "_data_cache", None)

        if data is None:
            data = self()
            self._data_cache = data

        if field_name in data:
            return data[field_name], self.toml_path.as_posix(), True

        return None, self.toml_path.as_posix(), False

    def __call__(self) -> dict[str, t.Any]:
        """Load settings from TOML file."""  # noqa: DOC201
        if not self.toml_path.exists():
            click.echo("[WARN] Settings file not found. Default values will be used.")
            click.echo(f"[INFO] Looking for settings file at: {self.toml_path}")
            return {}

        with self.toml_path.open("rb") as f:
            data = tomllib.load(f)

        return {k.upper(): v for k, v in data.items()}

    def __repr__(self) -> str:
        """Representation."""  # noqa: DOC201
        return f"TomlConfigSettingsSource(toml_path={self.toml_path})"


_no_config_msg = "Config has not been initialized."
_current_config: ContextVar[Settings] = ContextVar("current_config")


def setup_config(toml_path: str) -> None:
    """Initialize the global config instance."""
    _current_config.set(Settings(toml_path=toml_path))  # pyright: ignore[reportCallIssue]


config = t.cast(Settings, LocalProxy(_current_config, unbound_message=_no_config_msg))

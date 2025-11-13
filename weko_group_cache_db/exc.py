#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Exceptions module for weko-group-cache-db."""


class WekoGroupCacheDbError(Exception):
    """Exception class for weko-group-cache-db."""

    def __init__(self, fqdn: str, origin: Exception | None = None) -> None:
        """Initialize the exception with an optional original exception.

        Args:
            fqdn (str): The FQDN related to the error.
            origin (Exception | None): The original exception, if any.

        """
        super().__init__(fqdn)
        self.fqdn = fqdn
        self.original = origin

    def __str__(self) -> str:  # noqa: D105
        return f"FQDN: {self.fqdn}, {self.original}"  # pragma: no cover

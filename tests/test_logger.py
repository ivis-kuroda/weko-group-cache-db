#
# Copyright (C) 2025 National Institute of Informatics.
#

import logging
import typing as t

from datetime import datetime
from unittest.mock import patch

from rich.logging import RichHandler
from werkzeug.local import LocalProxy

from weko_group_cache_db.logger import _log_time_format, logger as logger_proxy, setup_logger


# def _log_time_format(datetime: datetime) -> Text:
def test__log_time_format():
    dt = datetime.now()
    result = _log_time_format(dt)
    assert result.plain == dt.isoformat(timespec="milliseconds")


# def setup_logger(name: str = __name__) -> logging.Logger:
def test_setup_logger_default_name(set_test_config):
    set_test_config(LOG_LEVEL="INFO")
    logger = setup_logger()
    assert logger.name == "weko_group_cache_db.logger"
    assert logger.level == logging.INFO


def test_setup_logger_custom_name(set_test_config):
    set_test_config(LOG_LEVEL="INFO")
    logger = setup_logger("custom_logger")
    assert logger.name == "custom_logger"
    assert logger.level == logging.INFO


def test_setup_logger_error_level(set_test_config):
    set_test_config(LOG_LEVEL="ERROR")
    logger = setup_logger("error_logger")
    assert logger.level == logging.ERROR


def test_setup_logger_attach_handler(set_test_config):
    set_test_config(LOG_LEVEL="INFO")
    logger = setup_logger("handler_logger")
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], RichHandler)
    assert logger.handlers[0].level == logging.INFO
    assert logger.handlers[0].formatter
    assert logger.handlers[0].formatter._fmt == "%(message)s"


def test_logger(set_test_config):
    set_test_config(LOG_LEVEL="INFO")
    logger = setup_logger("weko_group_cache_db")
    assert t.cast(LocalProxy, logger_proxy)._get_current_object() is logger


def test_logger_development_mode(set_test_config):
    set_test_config(LOG_LEVEL="DEBUG", DEVELOPMENT=True)

    with patch("weko_group_cache_db.logger.install") as mock_install:
        setup_logger("dev_logger")
        mock_install.assert_called_once()

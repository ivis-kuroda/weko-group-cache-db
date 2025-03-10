from click.testing import CliRunner
from logging import INFO
import pytest
from _pytest.logging import LogCaptureFixture

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def test_logger(caplog: LogCaptureFixture):
    caplog.set_level(INFO)
    return caplog

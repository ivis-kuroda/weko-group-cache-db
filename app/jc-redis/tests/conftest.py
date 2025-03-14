import pytest
import subprocess

@pytest.fixture
def switch_to_sentinel():
    """Switch to sentinel for testing
    
    This fixture stops the redis container and starts the sentinel container
    for testing purposes. It will switch back to the redis container after the
    test is complete.
    """
    subprocess.run(['docker', 'compose', 'stop', 'redis'])
    subprocess.run(['docker', 'compose', '-f', '../../docker-compose-sentinel.yml', 'up', '-d'])
    yield
    subprocess.run(['docker', 'compose', '-f', '../../docker-compose-sentinel.yml', 'down'])
    subprocess.run(['docker', 'compose', 'start', 'redis'])


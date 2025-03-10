import pytest
import subprocess

@pytest.fixture
def use_redis_container():
    subprocess.run(['docker', 'compose', 'up', '-d'])
    yield
    subprocess.run(['docker', 'compose', 'down'])

@pytest.fixture
def use_sentinel_container():
    subprocess.run(['docker', 'compose', '-f', '../../docker-compose-sentinel.yml', 'up', '-d'])
    yield
    subprocess.run(['docker', 'compose', '-f', '../../docker-compose-sentinel.yml', 'down'])

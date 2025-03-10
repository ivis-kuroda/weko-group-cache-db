from setuptools import find_packages, setup

setup(
    name='get-groups',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='Registration of groups in the cache database',
    packages=find_packages(),
    install_requires=[
        'celery',
        'click',
        'redis',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'get-groups = get_groups.cli:get_groups'
        ]
    },
)
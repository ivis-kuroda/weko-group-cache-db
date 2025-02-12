from setuptools import find_packages, setup

setup(
    name='jc-redis',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Redis module for the app',
    packages=find_packages(),
    install_requires=[
        'redis',
    ],
    entry_points={},
)
from setuptools import find_packages, setup

setup(
    name='new-group',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A new group module for the app',
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    entry_points={
        'app.modules': [
            'new_group = new_group',
        ],
    },
)
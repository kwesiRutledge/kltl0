"""
setup.py
Description:
    A setup.py file used to make this package pip-installable.
    Taken from https://goodresearch.dev/setup.html
"""

from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
)
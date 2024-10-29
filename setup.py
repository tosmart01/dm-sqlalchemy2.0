#!/usr/bin/env python
"""
Setup for SQLAlchemy backend for DM
"""
from setuptools import find_packages, setup

setup_params = dict(
    name="sqlalchemy_dm",
    version='2.0.1',
    description="SQLAlchemy dialect for DM",
    author="Dameng",
    author_email="",
    keywords='DM SQLAlchemy',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "sqlalchemy.dialects":
            ["dm = sqlalchemy_dm.dmPython:DMDialect_dmPython", "dm.dmPython = sqlalchemy_dm.dmPython:DMDialect_dmPython"]
    },
    install_requires=['dmPython', 'sqlalchemy'],
)

if __name__ == '__main__':
    setup(**setup_params)

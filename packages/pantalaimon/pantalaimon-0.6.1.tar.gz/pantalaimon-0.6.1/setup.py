# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pantalaimon",
    version="0.6.1",
    url="https://github.com/matrix-org/pantalaimon",
    author="The Matrix.org Team",
    author_email="poljar@termina.org.uk",
    description=("A Matrix proxy daemon that adds E2E encryption "
                 "capabilities."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    packages=find_packages(),
    install_requires=[
        "attrs <= 19.3.0",
        "aiohttp <= 3.6.2",
        "appdirs <= 1.4.3",
        "click <= 7.1.1",
        "keyring <= 21.2.0",
        "logbook <= 1.5.3",
        "peewee <= 3.13.3",
        "janus <= 0.5.0",
        "cachetools >= 3.0.0"
        "prompt_toolkit>2<4",
        "typing;python_version<'3.5'",
        "matrix-nio[e2e] >= 0.8.0"
    ],
    extras_require={
        "ui": [
            "dbus-python <= 1.2.16",
            "PyGObject <= 3.36.0",
            "pydbus <= 0.6.0",
            "notify2 <= 0.3.1",
        ]
    },
    entry_points={
        "console_scripts": ["pantalaimon=pantalaimon.main:main",
                            "panctl=pantalaimon.panctl:main"],
    },
    zip_safe=False
)

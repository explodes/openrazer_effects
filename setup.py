#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

setup(
    name="openrazer_effects",
    description="Effects for OpenRazer",
    url="https://github.com/explodes/openrazer_effects",
    author="Evan Leis",
    version="1.0.1",
    packages=find_packages(".", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "dbus-python==1.2.4",
        "numpy==1.13.3",
        "pgi==0.0.11.1",
        "PyAudio==0.2.11",
        "six==1.11.0",
    ],
    scripts=["openrazer_effects"],
    license="GPLv2",
    setup_requires=[
        "pytest-runner==3.0"
    ],
    tests_require=[
        "pytest==3.2.3",
    ],
    python_requires=">=3.6",
    zip_safe=True,
)

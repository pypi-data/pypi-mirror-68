#!/usr/bin/env python3

"""The setup script."""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

with open(here / "yaqd_seabreeze" / "VERSION") as version_file:
    version = version_file.read().strip()


with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = ["yaqd-core>=2020.05.1", "seabreeze", "pyusb", "numpy"]

extra_requirements = {"dev": ["black", "pre-commit"]}
extra_files = {"yaqd_seabreeze": ["VERSION"]}

setup(
    author="yaq Developers",
    author_email="git@ksunden.space",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    description="yaq daemons for Ocean Optics SeaBreeze spectrometers.",
    entry_points={
        "console_scripts": ["yaqd-seabreeze=yaqd_seabreeze._seabreeze:Seabreeze.main",],
    },
    install_requires=requirements,
    extras_require=extra_requirements,
    license="GNU Lesser General Public License v3 (LGPL)",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data=extra_files,
    keywords="yaqd-seabreeze",
    name="yaqd-seabreeze",
    packages=find_packages(include=["yaqd_seabreeze", "yaqd_seabreeze.*"]),
    url="https://gitlab.com/yaq/yaqd-seabreeze",
    version=version,
    zip_safe=False,
)

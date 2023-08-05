# Skidtools, A collection of utilities and tools to rapidly develop CLI programs. 
# It aims to get rid of boilerplate and aid skiddies.
# Copyright (C) 2020 Abdos

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Load list of dependencies
with open("requirements.txt") as data:
    install_requires = [
        line for line in data.read().split("\n")
            if line and not line.startswith("#")
    ]

setuptools.setup(
    name="skidtools", # Replace with your own username
    version="0.0.1a3",
    author="Abdos",
    author_email="admin.dev@clast.dev",
    description="A small utility package to reduce boilerplate code in skid scripts",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://docs.clast.dev/skidtools/",
    packages = setuptools.find_packages(exclude = ["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    python_requires='>=3.6',
    install_requires = install_requires
)
#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from importlib.metadata import version  # type: ignore

from ra_flatfile_importer import __version__
from ra_flatfile_importer import MOFlatFileFormat
from ra_flatfile_importer.mo_flatfile_gen import generate_mo_flatfile


def test_version():
    pyproject_version = version("ra-flatfile-importer")
    assert __version__ == pyproject_version


def test_mo_generate():
    flatfile1 = generate_mo_flatfile("Aarhus Kommune")
    assert type(flatfile1) == MOFlatFileFormat

    flatfile2 = generate_mo_flatfile("Aarhus Kommune")
    assert type(flatfile2) == MOFlatFileFormat
    assert flatfile1 == flatfile2

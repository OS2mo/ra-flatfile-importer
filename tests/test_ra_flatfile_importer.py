#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from ra_flatfile_importer import __version__
from ra_flatfile_importer import LoraFlatFileFormat
from ra_flatfile_importer import MOFlatFileFormat
from ra_flatfile_importer.lora_flatfile_gen import generate_lora_flatfile
from ra_flatfile_importer.mo_flatfile_gen import generate_mo_flatfile


def test_version():
    assert __version__ == "0.1.1"


def test_lora_generate():
    flatfile1 = generate_lora_flatfile("Aarhus Kommune")
    assert type(flatfile1) == LoraFlatFileFormat

    flatfile2 = generate_lora_flatfile("Aarhus Kommune")
    assert type(flatfile2) == LoraFlatFileFormat
    assert flatfile1 == flatfile2


def test_mo_generate():
    flatfile1 = generate_mo_flatfile("Aarhus Kommune")
    assert type(flatfile1) == MOFlatFileFormat

    flatfile2 = generate_mo_flatfile("Aarhus Kommune")
    assert type(flatfile2) == MOFlatFileFormat
    assert flatfile1 == flatfile2

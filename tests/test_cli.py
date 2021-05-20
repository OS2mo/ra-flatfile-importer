#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import pytest

from click.testing import CliRunner

from ra_flatfile_importer.flatfile_importer import cli


@pytest.mark.parametrize(
    "args,title,expected",
    [
        ([], "Flatfile importer.", [
            "lora  Lora Flatfile importer.",
            "mo    OS2mo Flatfile importer."
        ]),
        (["mo"], "OS2mo Flatfile importer.", [
            "generate  Generate OS2mo fixture.",
            "schema    Generate JSON schema for valid files.",
            "upload    Validate the provided JSON file and upload its contents.",
            "validate  Validate the provided JSON file.",
        ]),
        (["lora"], "Lora Flatfile importer.", [
            "generate    Generate LoRa fixture.",
            "initialize  Generate LoRa initializer file.",
            "schema      Generate JSON schema for valid files.",
            "upload      Validate the provided JSON file and upload its contents.",
            "validate    Validate the provided JSON file.",
        ]),
        (["lora", "schema", "--help"], "Generate JSON schema for valid files.", [
            "--indent INTEGER  Pass 'indent' to json serializer"
        ])
    ]
)
def test_cli(args, title, expected):
    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert title in result.output

    for command in expected:
        assert command in result.output

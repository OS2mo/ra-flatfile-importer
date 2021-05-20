#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import json
from contextlib import suppress as do_not_raise

import pytest
from click.testing import CliRunner

from ra_flatfile_importer.flatfile_importer import cli


@pytest.mark.parametrize(
    "args,title,expected",
    [
        (
            [],
            "Flatfile importer.",
            ["lora  Lora Flatfile importer.", "mo    OS2mo Flatfile importer."],
        ),
        (
            ["mo"],
            "OS2mo Flatfile importer.",
            [
                "generate  Generate OS2mo fixture.",
                "schema    Generate JSON schema for valid files.",
                "upload    Validate the provided JSON file and upload its contents.",
                "validate  Validate the provided JSON file.",
            ],
        ),
        (
            ["lora"],
            "Lora Flatfile importer.",
            [
                "generate    Generate LoRa fixture.",
                "initialize  Generate LoRa initializer file.",
                "schema      Generate JSON schema for valid files.",
                "upload      Validate the provided JSON file and upload its contents.",
                "validate    Validate the provided JSON file.",
            ],
        ),
        (
            ["lora", "schema", "--help"],
            "Generate JSON schema for valid files.",
            ["--indent INTEGER  Pass 'indent' to json serializer"],
        ),
    ],
)
def test_cli(args, title, expected):
    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert title in result.output

    for command in expected:
        assert command in result.output


@pytest.mark.parametrize(
    "args,expect_json",
    [
        ([], False),
        (["mo"], False),
        (["lora"], False),
        (["lora", "schema"], True),
        (["lora", "schema", "--help"], False),
        (["lora", "generate", "--name", "Aarhus Kommune"], True),
        (["lora", "initialize", "--name", "Aarhus Kommune"], True),
        (["lora", "validate", "--help"], False),
        (["lora", "upload", "--help"], False),
        (["mo", "schema"], True),
        (["mo", "generate", "--name", "Aarhus Kommune"], True),
        (["mo", "validate", "--help"], False),
        (["mo", "upload", "--help"], False),
    ],
)
def test_json_output(args, expect_json):
    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.exit_code == 0

    context_manager = do_not_raise()
    if not expect_json:
        context_manager = pytest.raises(json.decoder.JSONDecodeError)

    with context_manager:
        json.loads(result.output)

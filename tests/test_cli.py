#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import json
from contextlib import suppress as do_not_raise
from typing import Any

import pytest
from click.testing import CliRunner

from ra_flatfile_importer.cli import cli


@pytest.mark.parametrize(
    "args,expect_json",
    [
        ([], False),
        (["schema"], True),
        (["validate", "--help"], False),
        (["upload", "--help"], False),
    ],
)
def test_json_output(args, expect_json):
    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.exit_code == 0

    context_manager: Any = do_not_raise()
    if not expect_json:
        context_manager = pytest.raises(json.decoder.JSONDecodeError)

    with context_manager:
        json.loads(result.output)

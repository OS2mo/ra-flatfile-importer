#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import List

from ra_flatfile_importer.semantic_version_type import SemanticVersion

__version__: SemanticVersion = "0.1.0"

__lora_fileformat_version__: SemanticVersion = "0.1.0"
__supported_lora_fileformat_versions__: List[SemanticVersion] = ["0.1.0"]
assert (
    __lora_fileformat_version__ in __supported_lora_fileformat_versions__
), "Generated Lora version not supported"

__mo_fileformat_version__: SemanticVersion = "0.1.0"
__supported_mo_fileformat_versions__: List[SemanticVersion] = ["0.1.0"]
assert (
    __mo_fileformat_version__ in __supported_mo_fileformat_versions__
), "Generated MO version not supported"

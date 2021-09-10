#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from ra_utils.semantic_version_type import SemanticVersion

from ra_flatfile_importer.mo.models import MOFlatFileFormat
from ra_flatfile_importer.mo.models import MOFlatFileFormatChunk


__version__: SemanticVersion = SemanticVersion("1.0.0")

__all__ = [
    "__version__",
    "MOFlatFileFormat",
    "MOFlatFileFormatChunk",
]

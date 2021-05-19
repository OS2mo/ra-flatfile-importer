#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from itertools import chain
from typing import Iterator
from typing import List
from typing import Optional
from typing import Type
from typing import Literal

from pydantic import BaseModel, Extra
from ramodels.base import RABase
from ramodels.lora import Facet
from ramodels.lora import Klasse
from ramodels.lora import Organisation

from ra_flatfile_importer import __lora_fileformat_version__

# TODO: Change to from ramodels.mo import MOBase
LoraBase = Type[RABase]


class LoraFlatFileFormatChunk(BaseModel):
    """Flatfile chunk for LoRa.

    Each chunk in the list is send as bulk / in parallel, and as such entries
    within a single chunk should not depend on other entries within the same chunk.

    Minimal valid example is {}.
    """

    class Config:
        frozen = True
        extra = Extra.forbid

    facetter: Optional[List[Facet]]
    klasser: Optional[List[Klasse]]
    organisation: Optional[Organisation]


class LoraFlatFileFormat(BaseModel):
    """Flatfile format for LoRa.

    Each chunk in the list is send as bulk / in parallel, and as such entries
    within a single chunk should not depend on other entries within the same chunk.

    Minimal valid example is [].
    """

    class Config:
        frozen = True
        extra = Extra.forbid

    chunks: List[LoraFlatFileFormatChunk]
    version: Literal[__lora_fileformat_version__]

    def __iter__(self):
        return iter(self.chunks)

    def __getitem__(self, item):
        return self.chunks[item]


def concat_chunk(chunk: LoraFlatFileFormatChunk) -> Iterator[LoraBase]:
    """Convert a chunk to an iterator of objects."""
    return chain(
        [chunk.organisation] if chunk.organisation else [],
        chunk.facetter or [],
        chunk.klasser or [],
    )

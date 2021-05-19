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

from pydantic import BaseModel
from pydantic import Extra
from pydantic import validator
from ramodels.base import RABase
from ramodels.mo import Address
from ramodels.mo import Employee
from ramodels.mo import Engagement
from ramodels.mo import EngagementAssociation
from ramodels.mo import Manager
from ramodels.mo import OrganisationUnit
from semantic_version_type import SemanticVersion

from ra_flatfile_importer import __supported_mo_fileformat_versions__

# TODO: Change to from ramodels.mo import MOBase
MOBase = Type[RABase]


class MOFlatFileFormatChunk(BaseModel):
    """Flatfile chunk for OS2mo.

    Each chunk in the list is send as bulk / in parallel, and as such entries
    within a single chunk should not depend on other entries within the same chunk.

    Minimal valid example is {}.
    """

    class Config:
        frozen = True
        extra = Extra.forbid

    org_units: Optional[List[OrganisationUnit]]
    employees: Optional[List[Employee]]
    engagements: Optional[List[Engagement]]
    address: Optional[List[Address]]
    manager: Optional[List[Manager]]
    engagement_associations: Optional[List[EngagementAssociation]]


class MOFlatFileFormat(BaseModel):
    """Flatfile format for OS2mo.

    Each chunk in the list is send as bulk / in parallel, and as such entries
    within a single chunk should not depend on other entries within the same chunk.

    Minimal valid example is [].
    """

    class Config:
        frozen = True
        extra = Extra.forbid

    chunks: List[MOFlatFileFormatChunk]
    version: SemanticVersion

    @validator("version", pre=True, always=True)
    def check_version(cls, v):
        if v not in __supported_mo_fileformat_versions__:
            raise ValueError("fileformat version not supported")
        return v

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


def concat_chunk(chunk: MOFlatFileFormatChunk) -> Iterator[MOBase]:
    """Convert a chunk to an iterator of objects."""
    return chain(
        chunk.org_units or [],
        chunk.employees or [],
        chunk.engagements or [],
        chunk.address or [],
        chunk.manager or [],
        chunk.engagement_associations or [],
    )

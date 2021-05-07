#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import List

from pydantic import BaseModel
from ramodels.mo import Address
from ramodels.mo import Employee
from ramodels.mo import Engagement
from ramodels.mo import EngagementAssociation
from ramodels.mo import Manager
from ramodels.mo import OrganisationUnit


class MOFlatFileFormatModel(BaseModel):
    """Flatfile format for OS2mo.

    Minimal valid example is {}.
    """

    org_units: List[OrganisationUnit] = []
    employees: List[Employee] = []
    engagements: List[Engagement] = []
    address: List[Address] = []
    manager: List[Manager] = []
    engagement_associations: List[EngagementAssociation] = []

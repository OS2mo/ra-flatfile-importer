#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from uuid import UUID

from mo_flatfile_model import MOFlatFileFormatModel
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit

# from ramodels.mo import Address
# from ramodels.mo import Engagement
# from ramodels.mo import EngagementAssociation
# from ramodels.mo import Manager


def generate_mo_flatfile():
    flatfile = MOFlatFileFormatModel(
        org_units=[
            OrganisationUnit.from_simplified_fields(
                uuid=UUID("d9f707b6-af2d-49a3-92e7-ad3e9bd81e7d"),
                user_key="Toplevel",
                name="Top niveau",
                org_unit_type_uuid=UUID("d9f707b6-af2d-49a3-92e7-ad3e9bd81e7d"),
                org_unit_level_uuid=UUID("d9f707b6-af2d-49a3-92e7-ad3e9bd81e7d"),
            )
        ],
        employees=[
            Employee(
                uuid=UUID("1b0c7093-fd8d-45a8-8b46-5327ecbcd780"),
                name="John Deere",
            )
        ],
        engagements=[],
        address=[],
        manager=[],
        engagement_associations=[],
    )
    return flatfile

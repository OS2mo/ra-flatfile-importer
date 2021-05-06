from typing import List
from uuid import UUID

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


def generate_mo_flatfile():
    flatfile = MOFlatFileFormatModel(
        org_units = [
            OrganisationUnit.from_simplified_fields(
                uuid=UUID("d9f707b6-af2d-49a3-92e7-ad3e9bd81e7d"),
                user_key="Toplevel",
                name="Top niveau",
                org_unit_type_uuid=UUID("d9f707b6-af2d-49a3-92e7-ad3e9bd81e7d"),
                org_unit_level_uuid=UUID("d9f707b6-af2d-49a3-92e7-ad3e9bd81e7d"),
            )
        ],
        employees = [
            Employee.from_simplified_fields(
                uuid=UUID("1b0c7093-fd8d-45a8-8b46-5327ecbcd780"),
                name="John Deere",
                user_key="JD",
            )
        ],
        engagements = [],
        address = [],
        manager = [],
        engagement_associations = [],
    )

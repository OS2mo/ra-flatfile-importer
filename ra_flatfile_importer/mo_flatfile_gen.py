#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from functools import partial
from itertools import chain
from uuid import UUID

from fixture_data import get_class_map
from mimesis import Address as gen_address
from mimesis import Datetime as gen_datetime
from mimesis import Person as gen_person
from mimesis.builtins import DenmarkSpecProvider
from mimesis.enums import Gender
from mo_flatfile_model import MOFlatFileFormatModel
from ramodels.mo import Address
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from util import generate_uuid

# from ramodels.mo import Engagement
# from ramodels.mo import EngagementAssociation
# from ramodels.mo import Manager


def even(x: int) -> bool:
    return (x % 2) == 0


def generate_mo_flatfile(name: str, num_employees: int = 100):
    seed = name
    org_uuid = generate_uuid(seed)

    person = gen_person("da")
    address = gen_address("da")
    datetime = gen_datetime("da")

    spec_provider = DenmarkSpecProvider()

    org_uuid = "6d9c5332-1f68-9046-0003-d027b0963ba5"
    class_map = get_class_map(seed)

    def gen_post_address():
        return (
            address.street_name()
            + " "
            + address.street_number()
            + ", "
            + address.postal_code()[3:]
            + " "
            + address.city()
        )

    def create_employee(_: int) -> Employee:
        cpr = spec_provider.cpr()

        gender = Gender.MALE
        if even(int(cpr[-1])):
            gender = Gender.FEMALE

        name = person.full_name(gender=gender)

        return Employee(
            uuid=generate_uuid(seed + cpr),
            name=name,
            cpr_no=cpr,
        )

    def create_employee_address(
        employee: Employee, class_uuid, generator_func
    ) -> Address:
        value = generator_func()
        return Address.from_simplified_fields(
            uuid=generate_uuid(seed + employee.name + value),
            value=value,
            value2=None,
            address_type_uuid=class_uuid,
            org_uuid=org_uuid,
            from_date=datetime.date(start=1970, end=2010).isoformat(),
            person_uuid=employee.uuid,
        )

    create_phone_addresses = partial(
        create_employee_address,
        class_uuid=class_map["PhoneEmployee"],
        generator_func=partial(person.telephone, "########"),
    )
    create_email_addresses = partial(
        create_employee_address,
        class_uuid=class_map["EmailEmployee"],
        generator_func=person.email,
    )

    employees = list(map(create_employee, range(num_employees)))
    phone_numbers = list(map(create_phone_addresses, employees))
    email_addresses = list(map(create_email_addresses, employees))

    addresses = list(chain(phone_numbers, email_addresses))

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
        employees=employees,
        engagements=[],
        address=addresses,
        manager=[],
        engagement_associations=[],
    )
    return flatfile

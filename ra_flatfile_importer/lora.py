#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import cast
from typing import List
from typing import Type

import click
from pydantic import AnyHttpUrl
from pydantic import BaseModel
from raclients.lora import ModelClient
from ramodels.base import RABase
from ramodels.lora import Facet
from ramodels.lora import Klasse
from ramodels.lora import Organisation
from util import async_to_sync
from util import generate_uuid
from util import model_validate_helper
from util import takes_json_file
from util import validate_url

LoraObj = Type[RABase]


class LoraFlatFileFormatModel(BaseModel):
    """Flatfile format for LoRa.

    Minimal valid example is {}.
    """

    facetter: List[Facet] = []
    klasser: List[Klasse] = []
    organisationer: List[Organisation] = []


def lora_validate_helper(json_file) -> LoraFlatFileFormatModel:
    return cast(
        LoraFlatFileFormatModel,
        model_validate_helper(LoraFlatFileFormatModel, json_file),
    )


@click.group()
def lora() -> None:
    """Lora Flatfile importer.

    Used to validate and load flatfile data (JSON) into LoRa.
    """
    pass


@lora.command()
@takes_json_file
def validate(json_file) -> None:
    """Validate the provided JSON file."""
    lora_validate_helper(json_file)


@lora.command()
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def schema(indent: int) -> None:
    """Generate JSON schema for validate files."""
    click.echo(LoraFlatFileFormatModel.schema_json(indent=indent))


@lora.command()
@click.option(
    "--mox-url",
    default="http://localhost:8080",
    show_default=True,
    callback=validate_url,
    help="Address of the MOX host",
)
@takes_json_file
@async_to_sync
async def upload(json_file, mox_url: AnyHttpUrl) -> None:
    """Validate the provided JSON file and upload its contents."""
    flatfilemodel = lora_validate_helper(json_file)
    chunks = [
        flatfilemodel.organisationer,
        flatfilemodel.facetter,
        flatfilemodel.klasser,
    ]

    client = ModelClient(base_url=mox_url)
    async with client.context():
        for objs in chunks:
            await client.load_lora_objs(objs)


@lora.command()
@click.option(
    "--name",
    help="Name of the root organization",
    required=True,
)
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def initialize(name: str, indent: int) -> None:
    """Generate LoRa initializer file."""
    seed = name
    org_uuid = generate_uuid(seed)
    organisation = Organisation.from_simplified_fields(
        uuid=org_uuid,
        name=name,
        user_key=name,
    )
    org_unit_address_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "org_unit_address_type"),
        user_key="org_unit_address_type",
        organisation_uuid=org_uuid,
    )
    employee_address_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "employee_address_type"),
        user_key="employee_address_type",
        organisation_uuid=org_uuid,
    )
    address_property = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "address_property"),
        user_key="address_property",
        organisation_uuid=org_uuid,
    )
    engagement_job_function = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "engagement_job_function"),
        user_key="engagement_job_function",
        organisation_uuid=org_uuid,
    )
    org_unit_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "org_unit_type"),
        user_key="org_unit_type",
        organisation_uuid=org_uuid,
    )
    engagement_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "engagement_type"),
        user_key="engagement_type",
        organisation_uuid=org_uuid,
    )
    engagement_association_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "engagement_association_type"),
        user_key="engagement_association_type",
        organisation_uuid=org_uuid,
    )
    association_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "association_type"),
        user_key="association_type",
        organisation_uuid=org_uuid,
    )
    role_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "role_type"),
        user_key="role_type",
        organisation_uuid=org_uuid,
    )
    leave_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "leave_type"),
        user_key="leave_type",
        organisation_uuid=org_uuid,
    )
    manager_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "manager_type"),
        user_key="manager_type",
        organisation_uuid=org_uuid,
    )
    responsibility = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "responsibility"),
        user_key="responsibility",
        organisation_uuid=org_uuid,
    )
    manager_level = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "manager_level"),
        user_key="manager_level",
        organisation_uuid=org_uuid,
    )
    visibility = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "visibility"),
        user_key="visibility",
        organisation_uuid=org_uuid,
    )
    time_planning = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "time_planning"),
        user_key="time_planning",
        organisation_uuid=org_uuid,
    )
    org_unit_level = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "org_unit_level"),
        user_key="org_unit_level",
        organisation_uuid=org_uuid,
    )
    primary_type = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "primary_type"),
        user_key="primary_type",
        organisation_uuid=org_uuid,
    )
    org_unit_hierarchy = Facet.from_simplified_fields(
        uuid=generate_uuid(seed + "org_unit_hierarchy"),
        user_key="org_unit_hierarchy",
        organisation_uuid=org_uuid,
    )

    flatfile = LoraFlatFileFormatModel(
        facetter=[
            org_unit_address_type,
            employee_address_type,
            address_property,
            engagement_job_function,
            org_unit_type,
            engagement_type,
            engagement_association_type,
            association_type,
            role_type,
            leave_type,
            manager_type,
            responsibility,
            manager_level,
            visibility,
            time_planning,
            org_unit_level,
            primary_type,
            org_unit_hierarchy,
        ],
        organisationer=[organisation],
    )
    click.echo(flatfile.json(indent=indent))

#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import cast
from typing import List
from typing import Optional
from uuid import UUID

import click
from pydantic import AnyHttpUrl
from pydantic import BaseModel
from ramodels.mo import Address
from ramodels.mo import Employee
from ramodels.mo import Engagement
from ramodels.mo import EngagementAssociation
from ramodels.mo import Manager
from ramodels.mo import OrganisationUnit
from util import model_validate_helper
from util import takes_json_file
from util import validate_url


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


def mo_validate_helper(json_file) -> MOFlatFileFormatModel:
    return cast(
        MOFlatFileFormatModel, model_validate_helper(MOFlatFileFormatModel, json_file)
    )


@click.group()
def mo() -> None:
    """OS2mo Flatfile importer.

    Used to validate and load flatfile data (JSON) into OS2mo.
    """
    pass


@mo.command()
@takes_json_file
def validate(json_file) -> None:
    """Validate the provided JSON file."""
    mo_validate_helper(json_file)


@mo.command()
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def schema(indent: int) -> None:
    """Generate JSON schema for validate files."""
    click.echo(MOFlatFileFormatModel.schema_json(indent=indent))


@mo.command()
@click.option(
    "--mo-url",
    default="http://localhost:5000",
    show_default=True,
    callback=validate_url,
    help="Address of the OS2mo host",
)
@click.option(
    "--saml-token",
    type=click.UUID,
    help="Address of the OS2mo host",
)
@takes_json_file
def upload(json_file, mo_url: AnyHttpUrl, saml_token: Optional[UUID]) -> None:
    """Validate the provided JSON file and upload its contents."""
    flatfilemodel = mo_validate_helper(json_file)
    print(flatfilemodel)
    # TODO: Upload it using Client

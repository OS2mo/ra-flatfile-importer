#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import sys
import json

import click
from pydantic import BaseModel, ValidationError, AnyHttpUrl
from pydantic.tools import parse_obj_as


def load_file_as(model: BaseModel, json_file) -> BaseModel:
    json_data = json.load(json_file)
    return model.parse_obj(json_data)


def validate_url(ctx: click.Context, param: str, value: str) -> AnyHttpUrl:
    try:
        return parse_obj_as(AnyHttpUrl, value)
    except ValidationError as e:
        raise click.BadParameter(e)


def takes_json_file(function):
    function = click.option(
        "--json-file",
        help="JSON file of models to parse",
        type=click.File("r"),
        default=sys.stdin,
    )(function)
    return function


def model_validate_helper(model: BaseModel, json_file) -> BaseModel:
    try:
        return load_file_as(model, json_file)
    except json.decoder.JSONDecodeError:
        raise click.ClickException("Unable to parse input file as JSON")
    except ValidationError as e:
        raise click.ClickException(e)

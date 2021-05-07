#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import List

from pydantic import BaseModel
from ramodels.lora import Facet
from ramodels.lora import Klasse
from ramodels.lora import Organisation


class LoraFlatFileFormatModel(BaseModel):
    """Flatfile format for LoRa.

    Minimal valid example is {}.
    """

    facetter: List[Facet] = []
    klasser: List[Klasse] = []
    organisationer: List[Organisation] = []

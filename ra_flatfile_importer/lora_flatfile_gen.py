#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from fixture_data import gen_classes
from lora_flatfile_model import LoraFlatFileFormatModel
from ramodels.lora import Facet
from ramodels.lora import Klasse
from ramodels.lora import Organisation
from util import generate_uuid


def generate_lora_flatfile(
    name: str, dummy_classes: bool = False
) -> LoraFlatFileFormatModel:
    seed = name
    org_uuid = generate_uuid(seed)
    organisation = Organisation.from_simplified_fields(
        uuid=org_uuid,
        name=name,
        user_key=name,
    )
    facets = []
    klasses = []
    fixture_classes = gen_classes()
    for facet_bvn, classes in fixture_classes.items():
        facet = Facet.from_simplified_fields(
            uuid=generate_uuid(seed + facet_bvn),
            user_key=facet_bvn,
            organisation_uuid=org_uuid,
        )
        facets.append(facet)
        for clazz in classes:
            scope = "TEXT"
            if isinstance(clazz, tuple):
                user_key, title, scope = clazz
            else:
                title = clazz
                user_key = title
            klasse = Klasse.from_simplified_fields(
                facet_uuid=facet.uuid,
                uuid=generate_uuid(seed + facet_bvn + user_key),
                user_key=user_key,
                title=title,
                scope=scope,
                organisation_uuid=org_uuid,
            )
            klasses.append(klasse)

    flatfile = LoraFlatFileFormatModel(
        facetter=facets, klasser=klasses, organisation=organisation
    )
    return flatfile

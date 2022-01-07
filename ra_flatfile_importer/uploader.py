#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from pydantic import AnyHttpUrl
from ra_utils.headers import TokenSettings
from raclients.mo import ModelClient
from raclients.modelclientbase import common_session_factory
from tqdm import tqdm

from ra_flatfile_importer.models import concat_chunk
from ra_flatfile_importer.models import MOFlatFileFormatImport


async def upload(
    flat_file_import: MOFlatFileFormatImport,
    mo_url: AnyHttpUrl,
    client_id: str,
    client_secret: str,
    auth_server: AnyHttpUrl,
    auth_realm: str,
) -> None:
    client = ModelClient(
        base_url=mo_url,
        session_factory=common_session_factory(
            token_settings=TokenSettings(
                client_id=client_id,
                client_secret=client_secret,
                auth_realm=auth_realm,
                auth_server=auth_server,
            )
        ),
    )
    async with client.context():
        for chunk in tqdm(flat_file_import, desc="File chunks", unit="chunk"):
            objs = list(concat_chunk(chunk))
            if objs:
                await client.load_mo_objs(objs)

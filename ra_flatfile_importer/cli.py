# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import click

from ra_flatfile_importer.mo.cli import mo


@click.group()
def cli() -> None:
    """Flatfile importer.

    Used to validate and load flatfile data (JSON) into OS2mo.
    """
    pass


cli.add_command(mo)

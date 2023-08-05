#!/usr/bin/env python3

# Python standard library imports
import os
import typing

# Non-standard library python package imports
import click

# Imports of module(s) internal to this project/package
from blackjack import version
from blackjack.utils import greeting


NICKNAME_ENV_VAR = 'BLACKJACK_NICKNAME'


@click.command(
    context_settings=dict(
        help_option_names=['-h', '--help']
    )
)
@click.option(
    f"--{NICKNAME_ENV_VAR.replace('_', '-').lower()}", '-n', 'nickname',
    default=os.environ.get(NICKNAME_ENV_VAR, 'you'),
    type=str, required=True, hide_input=True, show_default=True,
    help=(
        'Your nickname in this blackjack game.'
        f"Can also be specified through environment variable '{NICKNAME_ENV_VAR}'."
    ),
)
@click.version_option(version=version)
@click.pass_context
def cli(
    ctx: typing.Any,
    nickname: str,
):
    click.echo(greeting(nickname))

#!/usr/bin/env python3

# Python standard library imports
import json
import os
import typing

# Non-standard library python package imports
import click

# Imports of module(s) internal to this project/package
from blackjack import version
from blackjack.game import main_loop
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
    type=str, required=True, hide_input=False, show_default=True,
    help=(
        'Your nickname in this blackjack game.'
        f"Can also be specified through environment variable '{NICKNAME_ENV_VAR}'."
    ),
)
@click.option(
    f"--shuffle-url", '-u', 'shuffle_url',
    default='http://nav-deckofcards.herokuapp.com/shuffle',
    type=str, required=True, hide_input=False, show_default=True,
    help=(
        'The URL to which this application will perform a HTTP GET method, '
        'expecting a JSON array of elements á la; '
        '`[...,{"suit":"CLUBS","value":"K"},{"suit":"SPADES","value":"8"},`'
    ),
)
@click.option(
    '--verbose', '-v', 'verbosity',
    type=int, count=True,
)
@click.option(
    '--quiet', '-q',
    type=int, count=True,
)
@click.version_option(version=version)
@click.pass_context
def cli(
    ctx: typing.Any,
    nickname: str,
    shuffle_url: str,
    verbosity: int,
    quiet: int,
):
    verbosity_level = verbosity - quiet
    if verbosity_level >= 2:
        local_vars = {**locals()}
        del local_vars['ctx']
        click.echo(
            json.dumps(local_vars, indent=2),
            err=True,
        )
    if verbosity_level >= 0:
        click.echo(greeting(nickname))

    main_loop(
        nickname=nickname,
        shuffle_url=shuffle_url,
        verbosity_level=verbosity - quiet,
    )

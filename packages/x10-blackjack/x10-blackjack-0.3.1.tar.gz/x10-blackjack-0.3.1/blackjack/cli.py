#!/usr/bin/env python3

# Python standard library imports
import os
import typing

# Non-standard library python package imports
import click
import requests

# Imports of module(s) internal to this project/package
from blackjack import version
from blackjack.game import (
    Card,
    CardSuit,
    CardValue,
)
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
@click.version_option(version=version)
@click.pass_context
def cli(
    ctx: typing.Any,
    nickname: str,
    shuffle_url: str,
):
    click.echo(greeting(nickname))
    shuffled_cards_json = requests.get(shuffle_url).json()
    shuffled_cards = [
        Card(
            value=CardValue[card_json['value']],
            suit=CardSuit[card_json['suit']],
        )
        for card_json
        in shuffled_cards_json
    ]
    click.echo(f"Here are the cards fetched from '{shuffle_url}' (in order);\n[")
    for card in shuffled_cards:
        click.echo(f"\t{str(card).title()},")
    click.echo(']')

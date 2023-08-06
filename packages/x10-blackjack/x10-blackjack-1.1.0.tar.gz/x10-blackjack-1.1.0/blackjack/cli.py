#!/usr/bin/env python3

# Python standard library imports
import json
import os
import textwrap
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
        help_option_names=['-h', '--help'],
        max_content_width=120,
    )
)
@click.option(
    f"--{NICKNAME_ENV_VAR.replace('_', '-').lower()}", '-n', 'nickname',
    default=os.environ.get(NICKNAME_ENV_VAR, 'you'),
    type=str, required=True, hide_input=False, show_default=True,
    metavar='"<player\'s nickname>"',
    help=textwrap.dedent(
        f"""\
        Your nickname in this blackjack game.

        Can also be specified through environment variable '{NICKNAME_ENV_VAR}'.
        """
    ),
)
@click.option(
    f"--shuffle-url", '-u', 'shuffle_url',
    default='http://nav-deckofcards.herokuapp.com/shuffle',
    type=str, required=True, hide_input=False, show_default=True,
    metavar='"<http URL to GET JSON array from>"',
    help=textwrap.dedent(
        """\
        The URL to which this application will perform a HTTP GET method.

        \b
        Expecting a JSON array of elements á la;
        `[
            ...,
            {"suit":"CLUBS","value":"K"},
            {"suit":"SPADES","value":"8"},
            ...,
        ]`
        """
    ),
)
@click.option(
    f"--player-draw-limit", '-l', 'player_draw_limit',
    default=17, type=int, required=True, hide_input=False, show_default=True,
    metavar='<draw limit>',
    help=textwrap.dedent(
        """\
        The amount of accumulated points after which you (the player) won't draw more cards if given the opportunity.
        """
    ),
)
@click.option(
    f"--auto-play", '-a', 'autoplay',
    default=False, is_flag=True, required=False, hide_input=False, show_default=True,
    help=textwrap.dedent(
        """\
        \b
        Set flag to have the program run in a loop of infinite blackjack games.

        (Until user interrupts with something like CTRL+C).
        """
    ),
)
@click.option(
    '--verbose', '-v', 'verbosity',
    type=int, count=True,
    help=textwrap.dedent(
        """\
        Verbosity level.

        \b
        Causes program to increase debug output during its execution.
        Multiple `-v`s increase verbosity.

        "Final level of verbosity" (V) is calculated as `V = verbosity - quiet`.
        """
    ),
)
@click.option(
    '--quiet', '-q',
    type=int, count=True,
    help=textwrap.dedent(
        """\
        Quiet/silence level.

        \b
        Causes program to silence debug output during its execution.
        Multiple `-q`s decrease verbosity.

        "Final level of verbosity" (V) is calculated as `V = verbosity - quiet`.
        """
    ),
)
@click.version_option(version=version)
@click.pass_context
def cli(
    # 'ctx' is required for click CliRunner integration tests
    #   when checking exit_code, and for when to exit program early.
    ctx: typing.Any,
    nickname: str,
    shuffle_url: str,
    player_draw_limit: int,
    autoplay: bool,
    verbosity: int,
    quiet: int,
):
    """
    Play blackjack against the (N)PC.

    This game of blackjack fetches deck of 52 (hopefully) unique and shuffled cards from specified URL endpoint.
    The game starts by handing out two cards to each player, first you, then your opponent.
    Thereafter, it's one card drawn at the time.
    The game lasts until either;
     - a player doesn't dare anymore (read: draw limit),
     - or oversteps by accumulating more than 21 points.
    """
    local_vars = {**locals()}
    del local_vars['ctx']
    local_vars['verbosity_level'] = verbosity - quiet
    if local_vars['verbosity_level'] >= 2:
        click.echo(
            json.dumps(local_vars, indent=2),
            err=True,
        )
    local_vars['ctx'] = ctx
    del local_vars['verbosity']
    del local_vars['quiet']
    if local_vars['verbosity_level'] >= 0:
        click.echo(greeting(nickname))

    main_loop(**local_vars)

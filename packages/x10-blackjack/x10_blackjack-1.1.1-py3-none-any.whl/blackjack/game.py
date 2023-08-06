#!/usr/bin/env python3

# Python standard library imports
import itertools
import random
import textwrap
import typing

# Non-standard library python package imports
import click
import requests
import tabulate

# Imports of module(s) internal to this project/package
from blackjack import (
    CardDeck,
    game_objects,
)
from blackjack.utils import ascertain_winner


def get_new_shuffled_deck(
    *,
    no_internet: bool = False,
    verbosity_level: int = 0,
    shuffle_url: str = 'http://nav-deckofcards.herokuapp.com/shuffle',
    **kwargs,
) -> CardDeck:
    if no_internet:
        shuffled_deck: CardDeck = random.sample(
            [
                game_objects.Card(
                    value=v,
                    suit=s,
                )
                for s, v
                in itertools.product(
                    [s for s in game_objects.CardSuit],
                    [v for v in game_objects.CardValue],
                )
            ],
            52,
        )
    else:
        if verbosity_level >= 1:
            click.echo(
                f"\tFetching shuffled deck of cards from '{shuffle_url}'...",
                err=True,
            )
        shuffled_cards_data = requests.get(shuffle_url).json()
        shuffled_deck: CardDeck = [
            game_objects.Card.from_json(json_card_data)
            for json_card_data
            in shuffled_cards_data
        ]
    if verbosity_level >= 2:
        click.echo(
            f"\tHere are the cards in deck to be used (in order);\n\t[",
            err=True,
        )
        for card in shuffled_deck:
            click.echo(f"\t\t{str(card)},", err=True)
        click.echo('\t]', err=True)
    if verbosity_level >= 1:
        click.echo(f"{len(shuffled_deck)} cards in deck!")
    return list(shuffled_deck)


def main_loop(
    **kwargs,
) -> None:
    """
    Outer main loop which accommodates re-playability.

    Without having to re-start the program as a whole.
    """
    while True:
        game_loop(
            shuffled_deck=get_new_shuffled_deck(**kwargs),
            **kwargs,
        )
        if kwargs['autoplay']:
            click.echo(
                '`--auto-play` flag set, continuing until interrupt (e.g. CTRL+C).',
                err=True,
            )
            continue
        if not click.confirm('\nDo you want to continue?', default=True):
            # User doesn't want to continue playing =)
            break


def sum_points_in_hand(
    hand: CardDeck,
) -> int:
    return sum(
        [
            card.points
            for card
            in hand
        ]
    )


def pick_from_top_of_deck(
    amount: int,
    deck_to_pick_from: CardDeck,
) -> typing.Tuple[
    CardDeck,
    CardDeck,
]:
    type_err_msg = (
        f"`amount` must be a natural number greater than zero, not '{amount}'"
    )
    if type(amount) is not int:
        raise TypeError(type_err_msg)
    elif amount < 1:
        raise ValueError(type_err_msg)

    if len(deck_to_pick_from) == 0:
        raise ValueError(
            '`deck_to_pick_from` must contain one or more `Card`s.'
        )

    return (
        deck_to_pick_from[:amount],
        deck_to_pick_from[amount:],
    )


def inner_game_loop_sequential_draws(    # noqa: C901
    input_deck: CardDeck,
    player_draw_limit: int,
    *,
    verbosity_level: int = 0,
) -> typing.Tuple[CardDeck, CardDeck]:
    """
    This function simulates the actual game.

    First the player draws up to (but not including) the specified draw limit.

    Then, the opponent draws cards either until the player is beat, or accumulated points are above 21.
    (The opponent doesn't draw cards when player has overextended - e.g. has more than 21 points accumulated).
    """
    # Initial draw, hard-coded to two cards each
    your_cards, input_deck = pick_from_top_of_deck(
        deck_to_pick_from=input_deck,
        amount=2,
    )
    opponents_cards, input_deck = pick_from_top_of_deck(
        deck_to_pick_from=input_deck,
        amount=2,
    )

    if (
        sum_points_in_hand(opponents_cards) == 21
        or sum_points_in_hand(your_cards) == 21
    ):
        # Game was won right of off the bat, first round
        return your_cards, opponents_cards

    # `list(your_cards)` - so as to use .extend() in while-loop
    your_cards, your_rounds = list(your_cards), 1
    while sum_points_in_hand(your_cards) < player_draw_limit:
        your_new_cards, input_deck = pick_from_top_of_deck(
            deck_to_pick_from=input_deck,
            amount=1,
        )
        if verbosity_level >= 3:
            click.echo(f"\nYou now picked; {your_new_cards}")
        your_cards.extend(your_new_cards)
        your_rounds += 1
    your_current_points = sum_points_in_hand(your_cards)
    if verbosity_level >= 2:
        click.echo(f"Your hand is now; {your_cards}")

    if your_current_points > 21:
        return your_cards, opponents_cards

    # Again, ensure `opponents_cards` is an extensible sequence (list)
    opponents_cards, opponents_rounds = list(opponents_cards), 1
    while (
        sum_points_in_hand(opponents_cards) <= your_current_points
        and sum_points_in_hand(opponents_cards) < 21
    ):
        # Your opponent doesn't draw points when
        #   she/he already beats your accumulated points
        # Or when you've already overextended yourself
        opponents_new_cards, input_deck = pick_from_top_of_deck(
            deck_to_pick_from=input_deck,
            amount=1,
        )
        if verbosity_level >= 3:
            click.echo(f"\nOpponent now picked; {opponents_new_cards}")
        opponents_cards.extend(opponents_new_cards)
        opponents_rounds += 1
    if verbosity_level >= 2:
        click.echo(f"Opponents hand is now; {opponents_cards}")
        click.echo(
            f"{len(input_deck)} remaining after "
            f"{max(your_rounds, opponents_rounds)} round(s)"
        )
    if verbosity_level >= 3:
        click.echo(f"\nDeck now remains with; {input_deck}")

    return your_cards, opponents_cards


def game_loop(
    nickname: str,
    shuffled_deck: CardDeck,
    *,
    no_internet: bool = False,
    opponents_nickname: str = 'Magnus',
    verbosity_level: int = 0,
    player_draw_limit: int = 17,
    **kwargs,
):
    """
        Inner game loop, a winner is declared per loop/invocation of this function.
    """

    your_cards, opponents_cards = inner_game_loop_sequential_draws(
        input_deck=shuffled_deck,
        player_draw_limit=player_draw_limit,
    )
    if verbosity_level >= 1:
        total_game_rounds = -1  # Firs round both draw two cards
        total_game_rounds += max(len(your_cards), len(opponents_cards))
        click.echo(f"Game is over after {total_game_rounds}", err=True)

    your_game_result = dict(
        Player=nickname.title(),
        Points=sum_points_in_hand(your_cards),
        Hand=textwrap.dedent(
            f"""\
            '{"', '".join([str(c) for c in your_cards])}'\
            """
        ),
    )
    opponents_game_result = dict(
        Player=opponents_nickname.title(),
        Points=sum_points_in_hand(opponents_cards),
        Hand=textwrap.dedent(
            f"""\
            '{"', '".join([str(c) for c in opponents_cards])}'\
            """
        ),
    )
    tabulated_output_string = tabulate.tabulate(
        (your_game_result, opponents_game_result),
        headers='keys',
    )
    click.echo(
        ascertain_winner(
            your_points=your_game_result['Points'],
            your_nickname=your_game_result['Player'],
            opponents_points=opponents_game_result['Points'],
            opponents_nickname=opponents_game_result['Player'],
        )
    )
    click.echo(tabulated_output_string)

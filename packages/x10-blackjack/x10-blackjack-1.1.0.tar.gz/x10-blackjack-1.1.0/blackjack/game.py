#!/usr/bin/env python3

# Python standard library imports
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


def main_loop(
    *args,
    **kwargs,
) -> None:
    """
    Outer main loop which accommodates re-playability.

    Without having to re-start the program as a whole.
    """
    while True:
        game_loop(*args, **kwargs)
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
    if (
        type(amount) is not int
        or amount < 1
    ):
        raise TypeError(
            f"`amount` must be a natural number greater than zero, not '{amount}'"
        )

    return (
        deck_to_pick_from[:amount],
        deck_to_pick_from[amount:],
    )


def ascertain_winner(   # noqa: C901
    your_points: int,
    your_nickname: str,
    opponents_points: int,
    opponents_nickname: str,
) -> str:
    you_win = f"{your_nickname} won!"
    opponent_wins = f"{opponents_nickname} won!"

    if your_points == opponents_points == 21:
        # This is only possible on first draw
        #   Where each player must both pick one Ace each,
        #   in addition to a card worth 10 points.
        return 'Tie - both got 21.'
    elif your_points == 21:
        return you_win
    elif opponents_points == 21:
        return opponent_wins

    # Now we know that nobody 'won' by getting 21
    #   Time to rule out losers, those who got more than 21
    if opponents_points > 21:
        return you_win
    elif your_points > 21:
        return opponent_wins

    # Now we're sure nobody got more than 21 points,
    #   time to ascertain winner
    if your_points < opponents_points:
        return opponent_wins
    return you_win


def inner_game_loop_sequential_draws(    # noqa: C901
    input_deck: CardDeck,
    player_draw_limit: int,
    *,
    verbosity_level: int = 0,
) -> typing.Tuple[CardDeck, CardDeck]:
    # Initial draw, hard-coded to two cards each
    your_cards, input_deck = pick_from_top_of_deck(
        deck_to_pick_from=input_deck,
        amount=2,
    )
    opponents_cards, input_deck = pick_from_top_of_deck(
        deck_to_pick_from=input_deck,
        amount=2,
    )

    # So as to use .extend() in while-loop
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

    # So as to use .extend() in while-loop
    opponents_cards, opponents_rounds = list(opponents_cards), 1
    while (
        sum_points_in_hand(opponents_cards) <= your_current_points
        or sum_points_in_hand(opponents_cards) < 21
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
    shuffle_url: str,
    *,
    opponents_nickname: str = 'Magnus',
    verbosity_level: int = 0,
    player_draw_limit: int = 17,
    **kwargs,
):
    """
        Inner game loop, a winner is declared per loop/invocation of this function.
    """
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
            f"\tHere are the cards fetched from '{shuffle_url}' (in order);\n\t[",
            err=True,
        )
        for card in shuffled_deck:
            click.echo(f"\t\t{str(card)},", err=True)
        click.echo('\t]', err=True)
    if verbosity_level >= 1:
        click.echo(f"{len(shuffled_deck)} cards received!")

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

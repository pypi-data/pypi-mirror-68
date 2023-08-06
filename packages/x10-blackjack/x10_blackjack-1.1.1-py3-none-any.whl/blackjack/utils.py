#!/usr/bin/env python3


def greeting(
    who_you_want_to_greet: str = None,
) -> str:
    who_you_want_to_greet = who_you_want_to_greet.strip()
    if (
        not isinstance(who_you_want_to_greet, str)
        or not(who_you_want_to_greet)
        or any(
            # If any of these remain in string
            # after strip()-ing the string...
            char in who_you_want_to_greet
            for char in ('\r', '\n')
        )
    ):
        who_you_want_to_greet = 'you'
    return f"Welcome to a game of blackjack, {who_you_want_to_greet}!"


def ascertain_winner(   # noqa: C901
    your_points: int,
    your_nickname: str,
    opponents_points: int,
    opponents_nickname: str,
) -> str:
    you_win = f"{your_nickname} won!"
    opponent_wins = f"{opponents_nickname} won!"

    if your_points == opponents_points:
        # This is only possible on first draw
        #   Where each player must both pick one Ace each,
        #   in addition to a card worth 10 points.
        return f"Tie - both got {your_points}."
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

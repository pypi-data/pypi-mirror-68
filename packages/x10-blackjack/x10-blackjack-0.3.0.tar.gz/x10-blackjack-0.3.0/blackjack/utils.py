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

#!/usr/bin/env python3


def greeting(
    who_you_want_to_greet: str = None,
) -> str:
    if (
        not isinstance(who_you_want_to_greet, str)
        or not(who_you_want_to_greet.strip())
    ):
        who_you_want_to_greet = 'you'
    return f"Welcome, {who_you_want_to_greet}!"

#!/usr/bin/env python3

# Python standard library imports
import typing

# Imports of module(s) internal to this project/package
from blackjack.game_objects import Card


# This value is not the one controlling the version in the (GitLab) pipeline
# This value is only necessary for automated pickup, and for manual deployments to PyPI
version = '1.0.0'

CardDeck = typing.Iterable[Card]

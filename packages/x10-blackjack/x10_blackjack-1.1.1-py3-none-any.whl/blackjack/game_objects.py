#!/usr/bin/env python3
"""
Sub-module defining the game objects required for blackjack;
 - a `Card`,
 - a card's `Suit`,
 - and a card's `Value`.
"""

# Python standard library imports
import dataclasses
import enum
import itertools
import json
import textwrap
import typing


CardValue = enum.Enum(
    value='CardValue',
    names=itertools.chain.from_iterable(
        itertools.product(v, (k,))
        for k, v
        in {
            enum.auto(): ('Ace', 'A',),
            enum.auto(): ('Two', '2',),
            enum.auto(): ('Three', '3',),
            enum.auto(): ('Four', '4',),
            enum.auto(): ('Five', '5',),
            enum.auto(): ('Six', '6',),
            enum.auto(): ('Seven', '7',),
            enum.auto(): ('Eight', '8',),
            enum.auto(): ('Nine', '9',),
            enum.auto(): ('Ten', '10',),
            enum.auto(): ('Jack', 'J',),
            enum.auto(): ('Queen', 'Q',),
            enum.auto(): ('King', 'K',),
        }.items()
    ),
)
CardSuit = enum.Enum(
    value='CardSuit',
    names=itertools.chain.from_iterable(
        itertools.product(v, (k,))
        for k, v
        in {
            enum.auto(): ('HEARTS', 'H',),
            enum.auto(): ('DIAMONDS', 'D',),
            enum.auto(): ('SPADES', 'S',),
            enum.auto(): ('CLUBS', 'C',),
        }.items()
    ),
)

# Used for type-hinting the `Card` class,
# within the method declaration of its own `classmethod`.
T = typing.TypeVar('T', bound='Card')


@dataclasses.dataclass(
    frozen=True,
    eq=True,
)
class Card:
    value: CardValue
    suit: CardSuit

    @property
    def points(self) -> int:
        map_of_points_per_value: typing.Dict[str, int] = {
            CardValue[str(v)]: v for v in range(2, 11)
        }
        map_of_points_per_value.update(
            {
                CardValue['J']: 10,
                CardValue['Q']: 10,
                CardValue['K']: 10,
                CardValue['A']: 11,
            }
        )
        return map_of_points_per_value[self.value]

    def __str__(self) -> str:
        return f"{self.value.name} of {self.suit.name.title()}"

    def __repr__(self) -> str:
        return textwrap.dedent(
            # The next two lines are crucial for `dedent()` to work.
            f"""\
            Card(
                value=CardValue['{self.value.name}'],
                suit=CardSuit['{self.suit.name}']
            )"""
        )

    @classmethod
    def from_json(
        cls: typing.Type[T],
        input_data: typing.Union[str, typing.Mapping],
    ) -> 'Card':    # ) -> T    # This alternative did not give desired type hint
        if isinstance(input_data, str):
            input_data = json.loads(input_data)     # pragma: no cover
        return cls(
            value=CardValue[input_data['value']],
            suit=CardSuit[input_data['suit'].upper()],
        )

    def to_json(self, **json_dumps_kwargs) -> str:
        class CardJsonEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Card):
                    return dict(
                        suit=obj.suit.name,
                        value=obj.value.name,
                    )
                # We don't care about testing the library-standard json
                # serialization behaviour...
                return json.JSONEncoder.default(self, obj)  # pragma: no cover
        json_dumps_kwargs['cls'] = CardJsonEncoder
        return json.dumps(
            self,
            **json_dumps_kwargs,
        )

    def __eq__(self, other) -> bool:
        return (
            self.value == other.value
            and self.suit == self.suit
        )

    def __lt__(self, other) -> bool:
        return self.points < other.points

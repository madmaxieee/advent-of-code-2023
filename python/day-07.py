from collections import Counter
from dataclasses import dataclass
from enum import Enum

__all__ = ["part_1", "part_2"]


def part_1(input: list[str]):
    hands = [Hand.from_string(line) for line in input]
    hands.sort()
    total_winning = sum(hand.bid * (i + 1) for i, hand in enumerate(hands))
    return total_winning


def part_2(input: list[str]):
    hands = [Hand.from_string(line.replace("J", "0")) for line in input]
    hands.sort()
    total_winning = sum(hand.bid * (i + 1) for i, hand in enumerate(hands))
    return total_winning


class HandType(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

    @classmethod
    def from_cards(cls, cards: list[int]):
        if 0 in cards:
            return cls.from_cards_joker(cards)
        else:
            return cls.from_cards_nomal(cards)

    @classmethod
    def from_cards_nomal(cls, cards: list[int]):
        card_counts = Counter(cards)
        card_count_counts = Counter(card_counts.values())
        if 5 in card_count_counts:
            return cls.FIVE_OF_A_KIND
        if 4 in card_count_counts:
            return cls.FOUR_OF_A_KIND
        if 3 in card_count_counts:
            if 2 in card_count_counts:
                return cls.FULL_HOUSE
            return cls.THREE_OF_A_KIND
        if 2 in card_count_counts:
            if card_count_counts[2] == 2:
                return cls.TWO_PAIR
            return cls.PAIR
        return cls.HIGH_CARD

    @classmethod
    def from_cards_joker(cls, cards: list[int]):
        card_counts = Counter(cards)
        card_count_counts = Counter(card_counts.values())
        if 5 in card_count_counts:
            return cls.FIVE_OF_A_KIND
        if 4 in card_count_counts:
            return cls.FIVE_OF_A_KIND
        if 3 in card_count_counts:
            if 2 in card_count_counts:
                return cls.FIVE_OF_A_KIND
            else:
                return cls.FOUR_OF_A_KIND
        if 2 in card_count_counts:
            if card_count_counts[2] == 2:
                if card_counts[0] == 1:
                    return cls.FULL_HOUSE
                if card_counts[0] == 2:
                    return cls.FOUR_OF_A_KIND
            else:
                return cls.THREE_OF_A_KIND
        return cls.PAIR


@dataclass
class Hand:
    cards: list[int]
    bid: int
    hand_type: HandType

    @classmethod
    def from_string(cls, line: str):
        cards_str, bid_str = line.split(" ")
        cards = [card_to_power(card) for card in cards_str]
        bid = int(bid_str)
        hand_type = HandType.from_cards(cards)
        return cls(cards, bid, hand_type)

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type.value < other.hand_type.value
        for self_card, other_card in zip(self.cards, other.cards):
            if self_card != other_card:
                return self_card < other_card
        return False

    def __repr__(self) -> str:
        return f"{self.hand_type} {self.cards} {self.bid}"


def card_to_power(card: str) -> int:
    if card == "T":
        return 10
    if card == "J":
        return 11
    if card == "Q":
        return 12
    if card == "K":
        return 13
    if card == "A":
        return 14
    return int(card)

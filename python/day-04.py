import re
from dataclasses import dataclass


def part_1(input: list[str]) -> str:
    cards = [ScratchCard.from_string(line) for line in input]
    total_score = sum(card.calculate_score() for card in cards)
    return str(total_score)


def part_2(input: list[str]) -> str:
    return "Part 2"


@dataclass
class ScratchCard:
    id: int
    winning_numbers: list[int]
    my_numbers: list[int]

    @classmethod
    def from_string(cls, line: str):
        matches = re.match(r"^Card\s+(\d+): (.*)\|(.*)", line)
        assert matches is not None
        groups = matches.groups()
        card_id = int(groups[0])
        winning_numbers = list(map(int, re.split(r"\s+", groups[1].strip())))
        my_numbers = list(map(int, re.split(r"\s+", groups[2].strip())))
        return cls(id=card_id, winning_numbers=winning_numbers, my_numbers=my_numbers)

    def calculate_score(self) -> int:
        score = 1
        for n in self.my_numbers:
            if n in self.winning_numbers:
                score *= 2
        return score // 2

import re
from dataclasses import dataclass


@dataclass
class GameStats:
    id: int
    rounds: list[dict[str, int]]


def parse_game(line: str):
    matches = re.match(r"^Game (\d+): (.*)", line)
    assert matches is not None
    groups = matches.groups()
    game_id = int(groups[0])
    rounds = [
        {
            tokens.split(" ")[1]: int(tokens.split(" ")[0])
            for tokens in round_str.split(", ")
        }
        for round_str in groups[1].split("; ")
    ]
    return GameStats(id=game_id, rounds=rounds)


def part_1(input: list[str]) -> str:
    num_cubes = {"red": 12, "green": 13, "blue": 14}
    solution = 0
    for line in input:
        game_stats = parse_game(line)
        for round in game_stats.rounds:
            for color, n in round.items():
                if n > num_cubes[color]:
                    break
            else:
                continue
            break
        else:
            solution += game_stats.id
    return str(solution)


def part_2(input: list[str]) -> str:
    return "Part 2"

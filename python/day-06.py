import math
from functools import reduce


def part_1(input: list[str]) -> str:
    times = [int(t) for t in input[0].split()[1:] if t.isdigit()]
    distances = [int(d) for d in input[1].split()[1:] if d.isdigit()]
    answer = reduce(
        lambda x, y: x * y,
        [calculate_win_times(t, d) for t, d in zip(times, distances)],
    )
    return str(answer)


def part_2(input: list[str]) -> str:
    time = int("".join(filter(str.isdigit, input[0])))
    distance = int("".join(filter(str.isdigit, input[1])))
    answer = calculate_win_times(time, distance)
    return str(answer)


def calculate_win_times(total_time: int, distance: int) -> int:
    d = math.sqrt(total_time * total_time - 4 * (distance + 1))
    low = math.ceil((total_time - d) / 2)
    high = math.floor((total_time + d) / 2)
    return high - low + 1

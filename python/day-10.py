from dataclasses import dataclass
from itertools import count
from typing import Literal

__all__ = ["part_1", "part_2"]


def part_1(input: list[str]):
    tiles = Tiles.parse_input(input)
    head_1 = tiles.start
    head_2 = tiles.start
    dir_1, dir_2 = [
        d
        for d in ("north", "south", "east", "west")
        if getattr(tiles.get(*tiles.start), d)
    ]
    assert dir_1 in ("north", "south", "east", "west")
    assert dir_2 in ("north", "south", "east", "west")
    for i in count():
        head_1, dir_1 = tiles.walk(head_1, dir_1)
        if head_1 == head_2:
            return i
        head_2, dir_2 = tiles.walk(head_2, dir_2)
        if head_1 == head_2:
            return i + 1


def part_2(input: list[str]):
    tiles = Tiles.parse_input(input)
    head_1 = tiles.start
    head_2 = tiles.start
    dir_1, dir_2 = [
        d
        for d in ("north", "south", "east", "west")
        if getattr(tiles.get(*tiles.start), d)
    ]
    assert dir_1 in ("north", "south", "east", "west")
    assert dir_2 in ("north", "south", "east", "west")

    is_loop = [[False] * len(tiles.pipes[0]) for _ in tiles.pipes]
    is_loop[tiles.start[0]][tiles.start[1]] = True
    while True:
        head_1, dir_1 = tiles.walk(head_1, dir_1)
        is_loop[head_1[0]][head_1[1]] = True
        if head_1 == head_2:
            break
        head_2, dir_2 = tiles.walk(head_2, dir_2)
        is_loop[head_2[0]][head_2[1]] = True
        if head_1 == head_2:
            break

    east_west_enclosed = set()
    for i in range(len(tiles.pipes)):
        current_row_north_count = 0
        current_row_south_count = 0
        for j in range(len(tiles.pipes[0])):
            tile = tiles.get(i, j)
            if is_loop[i][j]:
                if tile.north:
                    current_row_north_count += 1
                if tile.south:
                    current_row_south_count += 1
            else:
                if (
                    current_row_north_count % 2 == 1
                    and current_row_south_count % 2 == 1
                ):
                    east_west_enclosed.add((i, j))

    north_south_enclosed = set()
    for j in range(len(tiles.pipes[0])):
        current_col_east_count = 0
        current_col_west_count = 0
        for i in range(len(tiles.pipes)):
            tile = tiles.get(i, j)
            if is_loop[i][j]:
                if tile.east:
                    current_col_east_count += 1
                if tile.west:
                    current_col_west_count += 1
            else:
                if current_col_east_count % 2 == 1 and current_col_west_count % 2 == 1:
                    north_south_enclosed.add((i, j))

    enclosed = east_west_enclosed.intersection(north_south_enclosed)
    return len(enclosed)


Direction = Literal["north", "south", "east", "west"]


def opposite(direction: Direction) -> Direction:
    match direction:
        case "north":
            return "south"
        case "south":
            return "north"
        case "east":
            return "west"
        case "west":
            return "east"


@dataclass
class Pipe:
    north: bool
    south: bool
    east: bool
    west: bool
    shape: str

    @classmethod
    def from_str(cls, s: str):
        north = False
        south = False
        east = False
        west = False
        match s:
            case "|":
                north = True
                south = True
            case "-":
                east = True
                west = True
            case "7":
                south = True
                west = True
            case "L":
                north = True
                east = True
            case "J":
                north = True
                west = True
            case "F":
                south = True
                east = True
            case ".":
                pass
            case "S":
                pass
            case _:
                raise ValueError(f"Invalid character {s}")
        return cls(north, south, east, west, s)

    def __repr__(self):
        return f"Pipe(north={self.north}, south={self.south}, east={self.east}, west={self.west})"


@dataclass
class Tiles:
    pipes: list[list[Pipe]]
    start: tuple[int, int]

    @classmethod
    def parse_input(cls, input: list[str]):
        start = None
        pipes = []
        for i, line in enumerate(input):
            pipes.append([])
            for j, c in enumerate(line):
                if c == "S":
                    start = (i, j)
                pipes[-1].append(Pipe.from_str(c))
        assert start is not None
        if start[0] - 1 >= 0 and pipes[start[0] - 1][start[1]].south:
            pipes[start[0]][start[1]].north = True
        if start[0] + 1 < len(pipes) and pipes[start[0] + 1][start[1]].north:
            pipes[start[0]][start[1]].south = True
        if start[1] - 1 >= 0 and pipes[start[0]][start[1] - 1].east:
            pipes[start[0]][start[1]].west = True
        if start[1] + 1 < len(pipes[0]) and pipes[start[0]][start[1] + 1].west:
            pipes[start[0]][start[1]].east = True
        return cls(pipes, start)

    def walk(
        self,
        pos: tuple[int, int],
        direction: Direction,
    ) -> tuple[tuple[int, int], Direction]:
        if direction == "north":
            next_pos = (pos[0] - 1, pos[1])
        elif direction == "south":
            next_pos = (pos[0] + 1, pos[1])
        elif direction == "east":
            next_pos = (pos[0], pos[1] + 1)
        elif direction == "west":
            next_pos = (pos[0], pos[1] - 1)

        for d in ("north", "south", "east", "west"):
            if d == opposite(direction):
                continue
            if getattr(self.get(*next_pos), d):
                return next_pos, d

        raise AssertionError

    def get(self, x: int, y: int) -> Pipe:
        return self.pipes[x][y]

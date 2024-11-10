from collections import deque
from dataclasses import dataclass

__all__ = ["part_1", "part_2"]


def part_1(input: list[str]):
    input_queue = deque(input)
    seeds_line = input_queue.popleft()
    seeds = [int(s) for s in seeds_line.split(": ")[1].split()]
    input_queue.popleft()
    maps = Maps.parse(input_queue)
    min_location = min(maps.get_location(seed) for seed in seeds)
    return str(min_location)


def part_2(input: list[str]):
    input_queue = deque(input)
    seeds_line = input_queue.popleft()
    input_queue.popleft()
    nums = [int(s) for s in seeds_line.split(": ")[1].split()]
    seed_ranges = [Range(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)]
    maps = Maps.parse(input_queue)
    location_ranges = maps.get_location_ranges(seed_ranges)
    return str(location_ranges[0].head)


class Range:
    head: int
    len: int
    tail: int

    def __init__(self, head: int, len: int):
        self.head = head
        self.len = len
        self.tail = head + len
        assert self.len >= 0

    def __repr__(self):
        return f"[{self.head}, {self.tail})"


class MapEntry:
    dst: int
    src: int
    len: int
    dst_tail: int
    src_tail: int

    def __init__(self, dst: int, src: int, len: int):
        self.dst = dst
        self.src = src
        self.len = len
        self.dst_tail = dst + len
        self.src_tail = src + len
        assert self.len >= 0

    @classmethod
    def from_string(cls, line: str):
        nums = [int(n) for n in line.split()]
        assert len(nums) == 3
        return cls(nums[0], nums[1], nums[2])

    def __repr__(self):
        return f"[{self.src}, {self.src_tail}) -> [{self.dst}, {self.dst_tail})"


@dataclass
class Maps:
    seed2soil: list[MapEntry]
    soil2fertilizer: list[MapEntry]
    fertilizer2water: list[MapEntry]
    water2light: list[MapEntry]
    light2temperature: list[MapEntry]
    temperature2humidity: list[MapEntry]
    humidity2location: list[MapEntry]

    def get_location(self, seed: int) -> int:
        soil = lookup(self.seed2soil, seed)
        fertilizer = lookup(self.soil2fertilizer, soil)
        water = lookup(self.fertilizer2water, fertilizer)
        light = lookup(self.water2light, water)
        temperature = lookup(self.light2temperature, light)
        humidity = lookup(self.temperature2humidity, temperature)
        location = lookup(self.humidity2location, humidity)
        return location

    def get_location_ranges(self, seed_ranges: list[Range]) -> list[Range]:
        soil_ranges = map_ranges(self.seed2soil, seed_ranges)
        fertilizer_ranges = map_ranges(self.soil2fertilizer, soil_ranges)
        water_ranges = map_ranges(self.fertilizer2water, fertilizer_ranges)
        light_ranges = map_ranges(self.water2light, water_ranges)
        temperature_ranges = map_ranges(self.light2temperature, light_ranges)
        humidity_ranges = map_ranges(self.temperature2humidity, temperature_ranges)
        location_ranges = map_ranges(self.humidity2location, humidity_ranges)
        return location_ranges

    @classmethod
    def parse(cls, input: deque[str]):
        seed2soil = []
        soil2fertilizer = []
        fertilizer2water = []
        water2light = []
        light2temperature = []
        temperature2humidity = []
        humidity2location = []

        while len(input) > 0:
            line = input.popleft()
            if line.startswith("seed-to-soil "):
                seed2soil = cls.parse_map(input)
            elif line.startswith("soil-to-fertilizer "):
                soil2fertilizer = cls.parse_map(input)
            elif line.startswith("fertilizer-to-water "):
                fertilizer2water = cls.parse_map(input)
            elif line.startswith("water-to-light "):
                water2light = cls.parse_map(input)
            elif line.startswith("light-to-temperature "):
                light2temperature = cls.parse_map(input)
            elif line.startswith("temperature-to-humidity "):
                temperature2humidity = cls.parse_map(input)
            elif line.startswith("humidity-to-location "):
                humidity2location = cls.parse_map(input)

        return cls(
            seed2soil,
            soil2fertilizer,
            fertilizer2water,
            water2light,
            light2temperature,
            temperature2humidity,
            humidity2location,
        )

    @staticmethod
    def parse_map(input: deque[str]) -> list[MapEntry]:
        map_entries = []
        while len(input) > 0:
            line = input.popleft()
            if line == "":
                break
            map_entries.append(MapEntry.from_string(line))
        return sorted(map_entries, key=lambda entry: entry.src)


def lookup(map: list[MapEntry], key: int) -> int:
    for entry in map:
        if entry.src <= key < entry.src_tail:
            return entry.dst + key - entry.src
    return key


def map_range(entries: list[MapEntry], r: Range) -> list[Range]:
    if r.len == 0:
        return []
    result: list[Range] = []
    for e in entries:
        if e.src <= r.head < r.tail <= e.src_tail:
            result.append(Range(e.dst + r.head - e.src, r.len))
        elif e.src <= r.head < e.src_tail <= r.tail:
            result.append(Range(e.dst + r.head - e.src, e.src_tail - r.head))
            result.extend(map_range(entries, Range(e.src_tail, r.tail - e.src_tail)))
        elif r.head <= e.src < r.tail <= e.src_tail:
            result.append(Range(e.dst, r.tail - e.src))
            result.extend(map_range(entries, Range(r.head, e.src - r.head)))
        elif r.head <= e.src <= e.src_tail <= r.tail:
            result.append(Range(e.dst, e.len))
            result.extend(map_range(entries, Range(r.head, e.src - r.head)))
            result.extend(map_range(entries, Range(e.src_tail, r.tail - e.src_tail)))
    if len(result) == 0:
        result.append(r)
        return result
    result.sort(key=lambda r: r.head)
    merged_result = [result[0]]
    for r in result[1:]:
        if merged_result[-1].tail >= r.head:
            merged_result[-1].len = r.tail - merged_result[-1].head
        else:
            merged_result.append(r)
    return merged_result


def map_ranges(entries: list[MapEntry], ranges: list[Range]) -> list[Range]:
    result = []
    for r in ranges:
        result.extend(map_range(entries, r))
    return sorted(result, key=lambda r: r.head)

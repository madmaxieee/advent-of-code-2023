from collections import deque
from dataclasses import dataclass


def part_1(input: list[str]) -> str:
    input_queue = deque(input)
    seeds_line = input_queue.popleft()
    seeds = [int(s) for s in seeds_line.split(": ")[1].split()]
    input_queue.popleft()
    maps = Maps.parse(input_queue)
    min_location = min(maps.get_seed2location(seed) for seed in seeds)
    return str(min_location)


def part_2(input: list[str]) -> str:
    return "Part 2"


@dataclass
class MapEntry:
    dest_head: int
    src_head: int
    length: int

    @classmethod
    def from_string(cls, line: str):
        nums = [int(n) for n in line.split()]
        assert len(nums) == 3
        return cls(nums[0], nums[1], nums[2])


@dataclass
class Maps:
    seed2soil: list[MapEntry]
    soil2fertilizer: list[MapEntry]
    fertilizer2water: list[MapEntry]
    water2light: list[MapEntry]
    light2temperature: list[MapEntry]
    temperature2humidity: list[MapEntry]
    humidity2location: list[MapEntry]

    def get_seed2location(self, seed: int) -> int:
        soil = self.lookup(self.seed2soil, seed)
        fertilizer = self.lookup(self.soil2fertilizer, soil)
        water = self.lookup(self.fertilizer2water, fertilizer)
        light = self.lookup(self.water2light, water)
        temperature = self.lookup(self.light2temperature, light)
        humidity = self.lookup(self.temperature2humidity, temperature)
        location = self.lookup(self.humidity2location, humidity)
        return location

    @staticmethod
    def lookup(map: list[MapEntry], key: int) -> int:
        for entry in map:
            if entry.src_head <= key < entry.src_head + entry.length:
                return entry.dest_head + key - entry.src_head
        return key

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
        return map_entries

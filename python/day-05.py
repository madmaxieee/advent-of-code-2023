from collections import deque
from dataclasses import dataclass
from functools import lru_cache


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
class Maps:
    seed2soil: dict[int, int]
    soil2fertilizer: dict[int, int]
    fertilizer2water: dict[int, int]
    water2light: dict[int, int]
    light2temperature: dict[int, int]
    temperature2humidity: dict[int, int]
    humidity2location: dict[int, int]

    @lru_cache
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
    def lookup(map: dict[int, int], key: int) -> int:
        if key in map:
            return map[key]
        else:
            return key

    @classmethod
    def parse(cls, input: deque[str]):
        seed2soil = {}
        soil2fertilizer = {}
        fertilizer2water = {}
        water2light = {}
        light2temperature = {}
        temperature2humidity = {}
        humidity2location = {}

        while len(input) > 0:
            line = input.popleft()
            if line.startswith("seed-to-soil "):
                cls.parse_map(seed2soil, input)
            elif line.startswith("soil-to-fertilizer "):
                cls.parse_map(soil2fertilizer, input)
            elif line.startswith("fertilizer-to-water "):
                cls.parse_map(fertilizer2water, input)
            elif line.startswith("water-to-light "):
                cls.parse_map(water2light, input)
            elif line.startswith("light-to-temperature "):
                cls.parse_map(light2temperature, input)
            elif line.startswith("temperature-to-humidity "):
                cls.parse_map(temperature2humidity, input)
            elif line.startswith("humidity-to-location "):
                cls.parse_map(humidity2location, input)

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
    def parse_map(d: dict[int, int], input: deque[str]):
        while len(input) > 0:
            line = input.popleft()
            if line == "":
                break
            nums = [int(n) for n in line.split()]
            assert len(nums) == 3
            for i in range(nums[2]):
                d[nums[1] + i] = nums[0] + i

    def __hash__(self):
        return id(self)

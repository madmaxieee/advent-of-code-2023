import math
import re
from functools import reduce
from itertools import cycle
from typing import Callable, Self

__all__ = ["part_1", "part_2"]


def part_1(input: list[str]):
    instructions = list(input[0])
    graph = Graph()
    for line in input[2:]:
        graph.add_node_from_string(line)
    steps = graph.walk(instructions, "AAA", lambda s: s == "ZZZ")
    return steps


def part_2(input: list[str]):
    instructions = list(input[0])
    graph = Graph()
    starts = []
    for line in input[2:]:
        node = graph.add_node_from_string(line)
        if node.id.endswith("A"):
            starts.append(node.id)
    print(len(starts))
    lcm_steps = reduce(
        lambda x, y: x * y // math.gcd(x, y),
        (
            graph.walk(instructions, start, lambda s: s.endswith("Z"))
            for start in starts
        ),
    )
    return lcm_steps


class Node:
    id: str
    left: Self
    right: Self

    def __init__(self, node_id: str, left: Self | None, right: Self | None):
        self.id = node_id
        self.left = left if left else self
        self.right = right if right else self


class Graph:
    nodes: dict[str, Node]

    def __init__(self):
        self.nodes = {}

    def add_node_from_string(self, string: str) -> Node:
        matches = re.match(r"^([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", string)
        assert matches is not None
        groups = matches.groups()
        node_id = groups[0]
        left_id = groups[1]
        right_id = groups[2]

        if left_id not in self.nodes:
            self.nodes[left_id] = Node(left_id, None, None)
        if right_id not in self.nodes:
            self.nodes[right_id] = Node(right_id, None, None)

        if node_id not in self.nodes:
            self.nodes[node_id] = Node(
                node_id, self.nodes[left_id], self.nodes[right_id]
            )
        else:
            self.nodes[node_id].left = self.nodes[left_id]
            self.nodes[node_id].right = self.nodes[right_id]

        return self.nodes[node_id]

    def walk(
        self,
        instructions: list[str],
        start: str,
        is_target: Callable[[str], bool],
    ) -> int:
        current_node = self.nodes[start]
        for i, step in enumerate(cycle(instructions)):
            if step == "L":
                current_node = current_node.left
            elif step == "R":
                current_node = current_node.right
            if is_target(current_node.id):
                return i + 1
        raise ValueError("unreachable")

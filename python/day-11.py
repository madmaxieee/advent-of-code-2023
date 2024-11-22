from itertools import combinations

__all__ = ["part_1", "part_2"]


def part_1(input: list[str]):
    image = [list(row) for row in input]
    expanded_image = expand_image(image)
    galaxy_positions = []
    for i in range(len(expanded_image)):
        for j in range(len(expanded_image[i])):
            if expanded_image[i][j] == "#":
                galaxy_positions.append((i, j))
    total_distance = 0
    for a, b in combinations(range(len(galaxy_positions)), 2):
        g_a = galaxy_positions[a]
        g_b = galaxy_positions[b]
        total_distance += abs(g_a[0] - g_b[0]) + abs(g_a[1] - g_b[1])
    return total_distance


def part_2(input: list[str]):
    return "Part 2"


def expand_image(image: list[list[str]]):
    new_image = []
    empty_columns = {
        i
        for i in range(len(image[0]))
        if all(image[j][i] == "." for j in range(len(image)))
    }
    for row in image:
        new_row = []
        for i in range(len(row)):
            if i in empty_columns:
                new_row.append(row[i])
            new_row.append(row[i])
        new_image.append(new_row)
        if all(c == "." for c in row):
            new_image.append(new_row)
    return new_image


def print_image(image: list[list[str]]):
    for row in image:
        print("".join(row))
    print()

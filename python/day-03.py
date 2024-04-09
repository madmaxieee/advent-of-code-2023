ZERO = ord("0")
NINE = ord("9")


def part_1(input: list[str]) -> str:
    solution = 0
    for row, line in enumerate(input):
        curr_num = None
        curr_num_range = None
        for i, c in enumerate(line):
            if is_digit(c):
                if curr_num is None:
                    curr_num = int(c)
                    curr_num_range = (i, -1)
                else:
                    curr_num = curr_num * 10 + int(c)
            if not is_digit(c) or i == len(line) - 1:
                if curr_num is not None and curr_num_range is not None:
                    curr_num_range = (curr_num_range[0], i)
                    if check_surrounding(input, row, curr_num_range):
                        solution += curr_num
                    curr_num = None
                    curr_num_range = None
    return str(solution)


def part_2(input: list[str]) -> str:
    return "Part 2"


def check_surrounding(input: list[str], row: int, col_range: tuple[int, int]) -> bool:
    left, right = col_range
    for i in range(left - 1, right + 1):
        if i < 0 or i >= len(input[0]):
            continue
        if row - 1 >= 0 and is_symbol(input[row - 1][i]):
            return True
        if row + 1 < len(input) and is_symbol(input[row + 1][i]):
            return True
    if left - 1 >= 0 and is_symbol(input[row][left - 1]):
        return True
    if right < len(input[0]) and is_symbol(input[row][right]):
        return True
    return False


def is_digit(c: str):
    return ZERO <= ord(c) <= NINE


def is_symbol(c: str):
    return (not is_digit(c)) and c != "."

def part_1(input: list[str]) -> str:
    solution = 0
    zero = ord("0")
    nine = ord("9")
    for line in input:
        for c in line:
            ascii = ord(c)
            if zero <= ascii <= nine:
                solution += (ascii - zero) * 10
                break
        for c in reversed(line):
            ascii = ord(c)
            if zero <= ascii <= nine:
                solution += ascii - zero
                break
    return str(solution)


def part_2(input: list[str]) -> str:
    return "Part 2"

__all__ = ["part_1", "part_2"]


def part_1(input: list[str]):
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


def part_2(input: list[str]):
    solution = 0
    zero = ord("0")
    nine = ord("9")
    spelled_out_numbers = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    for line in input:
        for i, c in enumerate(line):
            ascii = ord(c)
            if zero <= ascii <= nine:
                solution += (ascii - zero) * 10
                break
            for n, word in enumerate(spelled_out_numbers):
                if line[i : i + len(word)] == word:
                    solution += (n + 1) * 10
                    break
            else:
                continue
            break
        reversed_line = line[::-1]
        for i, c in enumerate(reversed_line):
            ascii = ord(c)
            if zero <= ascii <= nine:
                solution += ascii - zero
                break
            for n, word in enumerate(spelled_out_numbers):
                if reversed_line[i : i + len(word)] == word[::-1]:
                    solution += n + 1
                    break
            else:
                continue
            break
    return str(solution)

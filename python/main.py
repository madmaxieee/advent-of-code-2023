import argparse
import os
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", type=int, required=True)
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-p", "--part", type=int, choices=[1, 2])
    args = parser.parse_args()

    input_file_path = get_input_file_path(args.day, args.test)

    with open(input_file_path) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    module = __import__(f"day-{args.day:02}")

    if args.part == 1 or args.part is None:
        start = time.time()
        solution_1 = module.part_1(lines)
        end = time.time()
        print("Part 1:", file=sys.stderr)
        print(solution_1)
        print(f"Time elapsed: {end - start:.6f}s", file=sys.stderr)

    if args.part is None:
        print()

    if args.part == 2 or args.part is None:
        start = time.time()
        solution_2 = module.part_2(lines)
        end = time.time()
        print("Part 2:", file=sys.stderr)
        print(solution_2)
        print(f"Time elapsed: {end - start:.6f}s", file=sys.stderr)


def get_input_file_path(day: int, test: bool) -> str:
    script_path = os.path.realpath(__file__)
    input_dir = os.path.join(os.path.dirname(script_path), "../inputs")
    file_name = f"day-{day:02}{'-test' if test else ''}.txt"
    return os.path.join(input_dir, file_name)


if __name__ == "__main__":
    main()

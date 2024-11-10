__all__ = ["part_1", "part_2"]


def part_1(input: list[str]):
    instabilities_list = [[int(num) for num in line.split(" ")] for line in input]
    total_instability_prediction = sum(
        predict(instabilities) for instabilities in instabilities_list
    )
    return total_instability_prediction


def part_2(input: list[str]):
    instabilities_list = [
        [int(num) for num in reversed(line.split(" "))] for line in input
    ]
    total_instability_prediction = sum(
        predict(instabilities) for instabilities in instabilities_list
    )
    return total_instability_prediction


def predict(nums: list[int]) -> int:
    next_diff = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    if all(diff == 0 for diff in next_diff):
        return nums[-1]
    return predict(next_diff) + nums[-1]

package madmaxieee.aoc2023;

import java.util.OptionalInt;

public class Day1 implements Solution {
    @Override
    public String solvePart1(final String input) {
        int sum = 0;
        for (final String line : input.split("\n")) {
            final int first_digit = firstDigitValue(line);
            final int last_digit = firstDigitValue(reverse(line));
            sum += first_digit * 10 + last_digit;
        }
        return Integer.toString(sum);
    }

    @Override
    public String solvePart2(final String input) {
        final String[] numbers = { "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" };
        final String[] reversed_numbers = { "eno", "owt", "eerht", "ruof", "evif", "xis", "neves", "thgie", "enin" };
        int sum = 0;
        for (String line : input.split("\n")) {
            final int first_number = firstNumberValue(line, numbers);
            final int last_number = firstNumberValue(reverse(line), reversed_numbers);
            sum += first_number * 10 + last_number;
        }
        return Integer.toString(sum);
    }

    private static String reverse(final String line) {
        return new StringBuilder(line).reverse().toString();
    }

    private static int firstDigitValue(final String line) {
        return line.chars().filter(Character::isDigit).findFirst().orElse('0') - '0';
    }

    private static int firstNumberValue(final String line, final String[] numbers) {
        int first_index = Integer.MAX_VALUE;
        OptionalInt first_value = OptionalInt.empty();
        for (int i = 0; i < line.length(); i++) {
            if (Character.isDigit(line.charAt(i))) {
                    first_index = i;
                    first_value = OptionalInt.of(line.charAt(i) - '0');
                break;
            }
        }
        for (int i = 0; i < numbers.length; i++) {
            final int index = line.indexOf(numbers[i]);
            if (index != -1 && index < first_index) {
                first_index = index;
                first_value = OptionalInt.of(i + 1);
            }
        }
        return first_value.orElseThrow();
    }
}

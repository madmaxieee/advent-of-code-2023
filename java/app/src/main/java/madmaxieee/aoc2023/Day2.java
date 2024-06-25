package madmaxieee.aoc2023;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class Day2 implements Solution {
    @Override
    public String solvePart1(final String input) {
        final int red_count = 12;
        final int blue_count = 14;
        final int green_count = 13;
        int sum = 0;
        for (String line : input.split("\n")) {
            Game game = Game.fromString(line);
            if (game.isPossible(red_count, blue_count, green_count)) {
                sum += game.id;
            }
        }
        return Integer.toString(sum);
    }

    @Override
    public String solvePart2(final String input) {
        int sum = 0;
        for (String line : input.split("\n")) {
            Game game = Game.fromString(line);
            int fewest_red = 0, fewest_blue = 0, fewest_green = 0;
            for (Round round : game.rounds) {
                fewest_red = Math.max(fewest_red, round.red);
                fewest_blue = Math.max(fewest_blue, round.blue);
                fewest_green = Math.max(fewest_green, round.green);
            }
            int power = fewest_red * fewest_blue * fewest_green;
            sum += power;
        }
        return Integer.toString(sum);
    }
}

class Round {
    final int red;
    final int blue;
    final int green;

    public Round(int red, int blue, int green) {
        this.red = red;
        this.blue = blue;
        this.green = green;
    }

    public String toString() {
        return String.format("%d red, %d blue, %d green", red, blue, green);
    }
}

class Game {
    final int id;
    final List<Round> rounds;

    public Game(int id) {
        this.id = id;
        this.rounds = new ArrayList<>();
    }

    public static Game fromString(String line) {
        String id_str = line.split(": ")[0].substring(5);
        int id = Integer.parseInt(id_str);
        Game game = new Game(id);
        String[] rounds = line.split(": ")[1].split("; ");
        Pattern pattern = Pattern.compile("(\\d+) (red|blue|green)");
        for (String round : rounds) {
            Matcher matcher = pattern.matcher(round);
            int red = 0, blue = 0, green = 0;
            while (matcher.find()) {
                int count = Integer.parseInt(matcher.group(1));
                String color = matcher.group(2);
                switch (color) {
                    case "red":
                        red = count;
                        break;
                    case "blue":
                        blue = count;
                        break;
                    case "green":
                        green = count;
                        break;
                    default:
                        break;
                }
            }
            game.rounds.add(new Round(red, blue, green));
        }
        return game;
    }

    public boolean isPossible(final int red_count, final int blue_count, final int green_count) {
        for (Round round : rounds) {
            if (round.red > red_count || round.blue > blue_count || round.green > green_count) {
                return false;
            }
        }
        return true;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Game ").append(id).append(": ");
        for (Round round : rounds) {
            sb.append(round).append("; ");
        }
        return sb.toString();
    }
}

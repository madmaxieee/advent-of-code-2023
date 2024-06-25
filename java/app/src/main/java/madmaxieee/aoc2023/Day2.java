package madmaxieee.aoc2023;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class Day2 implements Solution {

    private static final int RED_COUNT = 12;
    private static final int BLUE_COUNT = 14;
    private static final int GREEN_COUNT = 13;

    @Override
    public String solvePart1(final String input) {
        int sum = 0;
        for (String line : input.split("\n")) {
            Game game = Game.fromString(line);
            if (game.isPossible(RED_COUNT, BLUE_COUNT, GREEN_COUNT)) {
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
            int fewestRed = 0, fewestBlue = 0, fewestGreen = 0;
            for (Round round : game.rounds) {
                fewestRed = Math.max(fewestRed, round.red);
                fewestBlue = Math.max(fewestBlue, round.blue);
                fewestGreen = Math.max(fewestGreen, round.green);
            }
            int power = fewestRed * fewestBlue * fewestGreen;
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
    final static Pattern round_pattern = Pattern.compile("(\\d+) (red|blue|green)");

    public Game(int id) {
        this.id = id;
        this.rounds = new ArrayList<>();
    }

    public static Game fromString(String line) {
        String[] parts = line.split(": ");
        if (parts.length != 2) {
            throw new IllegalArgumentException("Invalid input: " + line);
        }

        int id;
        String id_str = parts[0].substring(5);
        try {
            id = Integer.parseInt(id_str);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Invalid game id: " + id_str);
        }

        Game game = new Game(id);
        String[] rounds = parts[1].split("; ");

        for (String round : rounds) {
            Matcher matcher = round_pattern.matcher(round);
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

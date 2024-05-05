const std = @import("std");
const config = @import("config");

const Allocator = std.mem.Allocator;
const List = std.ArrayList;
const Map = std.AutoHashMap;
const StrMap = std.StringHashMap;
const BitSet = std.DynamicBitSet;

const util = @import("util.zig");
const gpa = util.gpa;

pub fn main() !void {
    const data: []const u8 = comptime data: {
        if (config.use_test_data) {
            break :data @embedFile("inputs/day-01-test.txt");
        } else {
            break :data @embedFile("inputs/day-01.txt");
        }
    };
    if (config.part == 1 or config.part == 0) {
        print("Part 1:\n", .{});
        var t = try std.time.Timer.start();
        const answer1 = try part1(data);
        try util.stdout.print("{s}\n", .{answer1});
        print("Time elapsed: {}\n", .{std.fmt.fmtDuration(t.read())});
    }
    if (config.part == 2 or config.part == 0) {
        print("Part 2:\n", .{});
        var t = try std.time.Timer.start();
        const answer2 = try part2(data);
        try util.stdout.print("{s}\n", .{answer2});
        print("Time elapsed: {}\n", .{std.fmt.fmtDuration(t.read())});
    }
}

fn part1(data: []const u8) ![]u8 {
    var lines_iter = tokenizeAny(u8, data, "\n");
    var answer: u32 = 0;
    while (lines_iter.next()) |line| {
        {
            var i: usize = 0;
            while (i < line.len) : (i += 1) {
                const c: u8 = line[i];
                if (c >= '0' and c <= '9') {
                    answer += 10 * (c - '0');
                    break;
                }
            }
        }
        {
            var i: usize = 0;
            while (i < line.len) : (i += 1) {
                const c: u8 = line[line.len - 1 - i];
                if (c >= '0' and c <= '9') {
                    answer += c - '0';
                    break;
                }
            }
        }
    }
    return util.format("{}", .{answer});
}

fn part2(data: []const u8) ![]u8 {
    var lines_iter = tokenizeAny(u8, data, "\n");
    var answer: usize = 0;
    const number_strings = [_][]const u8{
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    };
    const NumPos = struct {
        pos: usize,
        val: usize,
    };
    while (lines_iter.next()) |line| {
        var current_num: usize = 0;
        {
            var first_number_pos: NumPos = .{
                .pos = std.math.maxInt(usize),
                .val = 0,
            };
            for (number_strings, 0..10) |number_string, i| {
                if (number_string.len > line.len) {
                    continue;
                }
                const pos = indexOfStr(u8, line, 0, number_string);
                if (pos != null and pos.? < first_number_pos.pos) {
                    first_number_pos = .{
                        .pos = pos.?,
                        .val = i,
                    };
                }
            }
            for (0..10) |i| {
                const pos = indexOf(u8, line, @truncate(i + '0'));
                if (pos != null and pos.? < first_number_pos.pos) {
                    first_number_pos = .{
                        .pos = pos.?,
                        .val = i,
                    };
                }
            }
            current_num += first_number_pos.val * 10;
        }
        {
            var last_number_pos: NumPos = .{
                .pos = 0,
                .val = 0,
            };
            for (number_strings, 0..10) |number_string, i| {
                if (number_string.len > line.len) {
                    continue;
                }
                const pos = lastIndexOfStr(u8, line, number_string);
                if (pos != null and pos.? >= last_number_pos.pos) {
                    last_number_pos = .{
                        .pos = pos.?,
                        .val = i,
                    };
                }
            }
            for (0..10) |i| {
                const pos = lastIndexOf(u8, line, @truncate(i + '0'));
                if (pos != null and pos.? >= last_number_pos.pos) {
                    last_number_pos = .{
                        .pos = pos.?,
                        .val = i,
                    };
                }
            }
            current_num += last_number_pos.val;
        }
        answer += current_num;
    }
    return util.format("{}", .{answer});
}

const tokenizeAny = std.mem.tokenizeAny;
const tokenizeSeq = std.mem.tokenizeSequence;
const tokenizeSca = std.mem.tokenizeScalar;
const splitAny = std.mem.splitAny;
const splitSeq = std.mem.splitSequence;
const splitSca = std.mem.splitScalar;
const indexOf = std.mem.indexOfScalar;
const indexOfAny = std.mem.indexOfAny;
const indexOfStr = std.mem.indexOfPosLinear;
const lastIndexOf = std.mem.lastIndexOfScalar;
const lastIndexOfAny = std.mem.lastIndexOfAny;
const lastIndexOfStr = std.mem.lastIndexOfLinear;
const trim = std.mem.trim;
const sliceMin = std.mem.min;
const sliceMax = std.mem.max;

const parseInt = std.fmt.parseInt;
const parseFloat = std.fmt.parseFloat;

const print = std.debug.print;
const assert = std.debug.assert;

const sort = std.sort.block;
const asc = std.sort.asc;
const desc = std.sort.desc;

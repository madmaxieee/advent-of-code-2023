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
    const data: []const u8 = data: {
        if (config.use_test_data) {
            break :data @embedFile("inputs/day-21-test.txt");
        } else {
            break :data @embedFile("inputs/day-21.txt");
        }
    };
    if (config.part == 1 or config.part == 0) {
        print("Part 1:\n", .{});
        var t = try std.time.Timer.start();
        const result1 = try part1(data);
        try util.stdout.print("{s}\n", .{result1});
        print("Time elapsed: {}\n", .{std.fmt.fmtDuration(t.read())});
    }
    if (config.part == 2 or config.part == 0) {
        print("Part 2:\n", .{});
        var t = try std.time.Timer.start();
        const result2 = try part2(data);
        try util.stdout.print("{s}\n", .{result2});
        print("Time elapsed: {}\n", .{std.fmt.fmtDuration(t.read())});
    }
}

fn part1(data: []const u8) ![]u8 {
    var lines_iter = tokenizeAny(u8, data, "\n");
    while (lines_iter.next()) |line| {
        _ = line;
    }
    return util.format("{}", .{null});
}

fn part2(data: []const u8) ![]u8 {
    var lines_iter = tokenizeAny(u8, data, "\n");
    while (lines_iter.next()) |line| {
        _ = line;
    }
    return util.format("{}", .{null});
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

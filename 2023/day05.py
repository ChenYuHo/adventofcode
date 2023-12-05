#!/usr/bin/env python
from os.path import join, dirname
from bisect import bisect_right
from itertools import pairwise


print("--- Advent of Code 2023 day 5 ---")

"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""


def adventofcode_day5_1(file):
    def src_to_dst(src, src_dst_map):
        dst_range_starts, src_range_starts, range_lens = src_dst_map
        rightmost_idx_le_src = bisect_right(src_range_starts, src) - 1
        if rightmost_idx_le_src < 0:
            return src
        if (
            src_range_starts[rightmost_idx_le_src] + range_lens[rightmost_idx_le_src]
            > src
        ):
            return (
                src
                - src_range_starts[rightmost_idx_le_src]
                + dst_range_starts[rightmost_idx_le_src]
            )
        return src

    seeds = []
    sorted_maps = []
    with open(file) as f:
        parsing_map = False
        list_of_lists = []
        for line in f:
            if parsing_map:
                if len(line) > 1:
                    list_of_lists.append(tuple(int(num) for num in line.split()))
                else:
                    sorted_maps.append(sorted(list_of_lists, key=lambda l: l[1]))
                    list_of_lists = []
                    parsing_map = False
                continue
            elif " map:" in line:
                parsing_map = True
            elif "seeds: " in line:
                seeds.extend(
                    int(seed) for seed in line.split(": ", maxsplit=1)[1].split()
                )
        if list_of_lists:
            sorted_maps.append(sorted(list_of_lists, key=lambda l: l[1]))

    min_location = float("inf")
    for seed in seeds:
        for src_dst_map in sorted_maps:
            seed = src_to_dst(seed, tuple(tuple(data) for data in zip(*src_dst_map)))
        min_location = min(seed, min_location)
    return min_location


print(adventofcode_day5_1(join(dirname(__file__), "day05_input.txt")))

"""
--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""


def adventofcode_day5_2(file):
    def src_start_len_pairs_to_dst_start_len_pairs(seed_ranges, mapping):
        destination_starts, source_starts, lengths = mapping
        result_ranges = []

        for seed_start, seed_len in seed_ranges:
            while seed_len > 0:
                # Find the rightmost source range that starts at or before the current seed
                rightmost_source_idx = bisect_right(source_starts, seed_start) - 1
                source_start = source_starts[rightmost_source_idx]
                source_end = source_start + lengths[rightmost_source_idx]

                if rightmost_source_idx < 0 or source_end <= seed_start:
                    # no covered at all, dst the same as src
                    result_ranges.append((seed_start, seed_len))
                    # continue next range
                    break

                destination_start = destination_starts[rightmost_source_idx]

                if source_end >= seed_start + seed_len:
                    # the entire range is covered by the source range
                    # Map the entire seed range to the destination range
                    result_ranges.append(
                        (destination_start + seed_start - source_start, seed_len)
                    )
                    break
                else:
                    # Only part of the seed range is covered by the source range
                    # Map the covered part to the destination range
                    covered_len = source_end - seed_start
                    result_ranges.append(
                        (destination_start + seed_start - source_start, covered_len)
                    )

                    # Move on to the uncovered part of the seed range
                    seed_start = source_end
                    seed_len -= covered_len

        return result_ranges

    seeds = []
    sorted_maps = []
    with open(file) as f:
        parsing_map = False
        list_of_lists = []
        for line in f:
            if parsing_map:
                if len(line) > 1:
                    list_of_lists.append(tuple(int(num) for num in line.split()))
                else:
                    sorted_maps.append(sorted(list_of_lists, key=lambda l: l[1]))
                    list_of_lists = []
                    parsing_map = False
                continue
            elif " map:" in line:
                parsing_map = True
            elif "seeds: " in line:
                range_lists = line.split(": ", maxsplit=1)[1].split()
                for i in range(0, len(range_lists), 2):
                    seeds.append((int(range_lists[i]), int(range_lists[i + 1])))
        if list_of_lists:
            sorted_maps.append(sorted(list_of_lists, key=lambda l: l[1]))

    min_location = float("inf")
    for range_start, range_len in seeds:
        queue = [(range_start, range_len)]
        for src_dst_map in sorted_maps:
            data = tuple(tuple(data) for data in zip(*src_dst_map))
            queue = src_start_len_pairs_to_dst_start_len_pairs(queue, data)
        min_location = min(min_location, min(queue)[0])

    return min_location


print(adventofcode_day5_2(join(dirname(__file__), "day05_input.txt")))

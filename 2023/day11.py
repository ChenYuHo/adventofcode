#!/usr/bin/env python
from os.path import join, dirname
from itertools import combinations
from bisect import bisect_left


print("--- Advent of Code 2023 day 11 ---")

"""
--- Day 11: Cosmic Expansion ---
You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

Your puzzle answer was 10231178.
"""


def adventofcode_day11_1(file):
    empty_row_indices = []
    empty_col_indices = []
    non_empty_col_indices = set()
    original_coordinates = []
    with open(file) as f:
        image = f.read().splitlines()

    for row, line in enumerate(image):
        empty_row = True
        for col, pixel in enumerate(line):
            if pixel == "#":
                empty_row = False
                non_empty_col_indices.add(col)
                original_coordinates.append((row, col))
        if empty_row:
            empty_row_indices.append(row)

    for col in range(len(image[0])):
        if col not in non_empty_col_indices:
            empty_col_indices.append(col)

    row_mappings = {}
    col_mappings = {}
    coordinates_after_expansion = []

    for row, col in original_coordinates:
        if row not in row_mappings:
            num_empty_rows_above = bisect_left(empty_row_indices, row)
            row_mappings[row] = row + num_empty_rows_above

        if col not in col_mappings:
            num_empty_cols_left = bisect_left(empty_col_indices, col)
            col_mappings[col] = col + num_empty_cols_left

        coordinates_after_expansion.append((row_mappings[row], col_mappings[col]))

    ans = 0
    for (row1, col1), (row2, col2) in combinations(coordinates_after_expansion, 2):
        ans += abs(row1 - row2) + abs(col1 - col2)

    return ans


print(adventofcode_day11_1(join(dirname(__file__), "day11_input.txt")))

"""
--- Part Two ---
The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

Your puzzle answer was 622120986954.
"""

# the only difference is calculation of coordinates_after_expansion, line 193 and 196
def adventofcode_day11_2(file):
    empty_row_indices = []
    empty_col_indices = []
    non_empty_col_indices = set()
    original_coordinates = []
    with open(file) as f:
        image = f.read().splitlines()

    for row, line in enumerate(image):
        empty_row = True
        for col, pixel in enumerate(line):
            if pixel == "#":
                empty_row = False
                non_empty_col_indices.add(col)
                original_coordinates.append((row, col))
        if empty_row:
            empty_row_indices.append(row)

    for col in range(len(image[0])):
        if col not in non_empty_col_indices:
            empty_col_indices.append(col)

    row_mappings = {}
    col_mappings = {}
    coordinates_after_expansion = []

    for row, col in original_coordinates:
        if row not in row_mappings:
            num_empty_rows_above = bisect_left(empty_row_indices, row)
            row_mappings[row] = row + num_empty_rows_above * (1000000 - 1)
        if col not in col_mappings:
            num_empty_cols_left = bisect_left(empty_col_indices, col)
            col_mappings[col] = col + num_empty_cols_left * (1000000 - 1)
        coordinates_after_expansion.append((row_mappings[row], col_mappings[col]))

    ans = 0
    for (row1, col1), (row2, col2) in combinations(coordinates_after_expansion, 2):
        ans += abs(row1 - row2) + abs(col1 - col2)

    return ans


print(adventofcode_day11_2(join(dirname(__file__), "day11_input.txt")))

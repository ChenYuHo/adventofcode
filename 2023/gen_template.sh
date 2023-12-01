#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"
if [[ -f day01.py ]]; then
  largest_day=$(ls day*.py | grep -oE '\d+' | sort -n | tail -n 1)
  next_day=$(printf "%02d" $((largest_day + 1)))
else
  next_day="01"
fi

non_padded=$((10#$next_day))
cat <<EOT > day${next_day}.py
#!/usr/bin/env python
from os.path import join, dirname


print("--- Advent of Code 2023 day ${non_padded} ---")

"""
Part 1 Problem Description
"""


def adventofcode_day${non_padded}_1(file):
    pass


print(adventofcode_day${non_padded}_1(join(dirname(__file__), "day${next_day}_input.txt")))

"""
Part 2 Problem Description
"""


def adventofcode_day${non_padded}_2(file):
    pass


print(adventofcode_day${non_padded}_2(join(dirname(__file__), "day${next_day}_input.txt")))

EOT
chmod +x day${next_day}.py
touch day${next_day}_input.txt

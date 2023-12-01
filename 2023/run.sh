#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
if [[ -n ${1} ]]; then
  temp="0"$1
  padded=${temp:(-2)}
  if [[ -f day$padded.py ]]; then
    echo "running the given day${padded}.py"
    /usr/bin/env python day${padded}.py
    exit 0
  else
    echo "day${padded}.py does not exist"
    exit 1
  fi
fi
if [[ -f day01.py ]]; then
  largest_day=$( ls day*.py | grep -oE '\d+' | sort -n | tail -n 1)
  echo "running latest day${largest_day}.py"
  /usr/bin/env python day${largest_day}.py
else
  echo "Nothing to run!"
  exit 1
fi


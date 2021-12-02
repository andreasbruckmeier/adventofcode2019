#!/usr/bin/env python3
import icc

with open('input.txt', 'r') as f:
  data = f.read().strip()

icc = icc.IntCodeComputer()
icc.load(data)

# patch for task1
icc.patch(1, 12)
icc.patch(2, 2)

icc.run()

print("Value at position 0:", icc.get(0))

#!/usr/bin/env python3
import icc

with open('input.txt', 'r') as f:
  data = f.read().strip()

icc = icc.IntCodeComputer()

for noun in range(0,100):
  for verb in range(0,100):
    icc.load(data)
    icc.patch(1, noun)
    icc.patch(2, verb)
    icc.run()
    if icc.get(0) == 19690720:
      print(100 * noun + verb)
      break

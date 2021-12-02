#!/usr/bin/env python3
import logging
import sys
import icc

from itertools import permutations

loglevel = 'INFO'
logger = logging.getLogger()
logger.setLevel(getattr(logging, loglevel))
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(getattr(logging, loglevel))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

with open('input.txt', 'r') as f:
  code = f.read().strip()

icc = icc.IntCodeComputer()
max_output = 0
for sequence in list(permutations([0,1,2,3,4],5)):
  output = 0
  for sequence in sequence:
    icc.load(code)
    icc.put_stdin(sequence)
    icc.put_stdin(output)
    icc.run()
    output = icc.read_stdout()
  if output > max_output:
    max_output = output
print(max_output)

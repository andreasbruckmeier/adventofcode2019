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

# task 1
icc = icc.IntCodeComputer()
icc.load(code)
icc.put_stdin(1)
icc.run()

print("BOOST keycode: {}".format(icc.read_stdout()))

# task 2
icc.load(code)
icc.put_stdin(2)
icc.run()

print("coordinates of the distress signal: {}".format(icc.read_stdout()))

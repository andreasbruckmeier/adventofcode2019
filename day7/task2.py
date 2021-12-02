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

# debug code
#code = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'

max_output = 0
for sequence in list(permutations([5,6,7,8,9],5)):

  # create 5 amplifiers with inital code set
  amplifiers = []
  for i in range(5):
    amplifiers.append(icc.IntCodeComputer().load(code).put_stdin(sequence[i]))

  i = 0
  output = 0
  while True:
    current_amp = amplifiers[i % 5]
    current_amp.put_stdin(output)
    current_amp.run()
    if current_amp.halted and i % 5 == 5 - 1:
      output = current_amp.read_stdout()
      # not sure if it supposed to not write something 
      # to stdoud in some cases, but by just setting output to 0 in those cases
      # we finally got the correct solution (keep this in mind)
      if not output:
        output = 0
        break
      if output > max_output:
        max_output = output
        break
    output = current_amp.read_stdout()
    i += 1

print(max_output)

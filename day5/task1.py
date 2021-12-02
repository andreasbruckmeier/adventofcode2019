#!/usr/bin/env python3
import logging
import sys
import icc

loglevel = 'INFO'
logger = logging.getLogger()
logger.setLevel(getattr(logging, loglevel))
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(getattr(logging, loglevel))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

with open('input.txt', 'r') as f:
  data = f.read().strip()

icc = icc.IntCodeComputer()
icc.load(data)

# After providing 1 to the only input instruction ...
icc.put_stdin(5)

icc.run()

print("stdout:", icc.read_stdout())

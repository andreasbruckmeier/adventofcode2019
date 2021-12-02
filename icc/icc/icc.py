#!/usr/bin/env python3
import logging

class IntCodeComputer:

  MEM_SIZE = 1048576

  def __init__(self):
    self.logger = logging.getLogger('int_code_computer')
    self.mem = [0] * IntCodeComputer.MEM_SIZE
    self.stdin = []
    self.stdout = []
    self.ptr = 0
    self.relative = 0
    self.halted = False

  def load(self, code):
    """ Load program code into the computers memory
        If code starts with a number, it is interpreted as
        a string of IntCode, otherwise as a filename
    """
    if code[0].isdigit():
      codelist = list(map(int, code.split(',')))
    else:
      with open(code, 'r') as f:
        codelist = list(map(int, f.read().strip().split(',')))
    self.mem = [0] * IntCodeComputer.MEM_SIZE
    for i in range(len(codelist)):
      self.mem[i] = codelist[i]
    self.stdin = []
    self.stdout = []
    self.ptr = 0
    self.relative = 0
    self.halted = False
    return self

  def dump(self):
    """ Returns the memory content until the first halt opcode.
        The condition has beed introduced on day 9 in order to
        avoid dumping loads of unused memory - use with care :)

        Day 9:
        "The computer's available memory should be much larger 
         than the initial program. Memory beyond the initial 
         program starts with the value 0 and can be read or 
         written like any other memory."
    """
    return self.mem[0:self.mem.index(99)+1]

  def put_stdin(self, value):
    """ Appends the given value to stdin
    """
    self.stdin.append(value)
    return self

  def read_stdout(self, return_all=False):
    """ Returns the oldest value from stdout and removes it
    """
    if self.stdout and not return_all:
      return self.stdout.pop(0)
    elif return_all:
      tmp = self.stdout
      self.stdout = []
      return tmp
    else:
      return None

  def run(self):
    """ This is the computer main loop
    """
    while self.ptr < len(self.mem):
      """ Value at current ptr position should always be an opcode
          It consists of up to 5 digits ABCDE starting from the right

          DE - two-digit opcode with leading zero
          C - mode of 1st parameter 
          B - mode of 2nd parameter
          A - mode of 3rd parameter

          Modes: 0: position mode, 1: immediate mode, 2: relative mode
      """
      op = self.mem[self.ptr] % 100
      m1 = self.mem[self.ptr] // 100 % 10
      m2 = self.mem[self.ptr] // 1000 % 10
      m3 = self.mem[self.ptr] // 10000

      self.logger.info('{:04d}: instr {} -> op: {}, m1: {}, m2: {}, m3: {}'. \
        format(self.ptr, self.mem[self.ptr], op, m1, m2, m3))

      if op == 1:
        self.add(m1, m2, m3)
      elif op == 2:
        self.mul(m1, m2, m3)
      elif op == 3:
        if not self.read(m1):
          # See comment within self.read() for the reason
          return
      elif op == 4:
        self.write(m1)
      elif op == 5:
        self.jump_if_true(m1, m2)
      elif op == 6:
        self.jump_if_false(m1, m2)
      elif op == 7:
        self.less_than(m1, m2, m3)
      elif op == 8:
        self.equals(m1, m2, m3)
      elif op == 9:
        self.adjust_relative(m1)
      elif op == 99:
        self.halted = True
        self.logger.info("halted")
        return

  def get_value(self, address, mode = 0):
    """ Returns the value stored on the translated memory address 
        according to the given mode.
    """
    return self.mem[self.mem[address] + self.relative] if mode == 2 \
      else self.mem[address] if mode == 1 else self.mem[self.mem[address]]

  def get_position(self, address, mode = 0):
    """ Returns the translated memory address according to the given mode.
    """
    return self.mem[address] + self.relative if mode == 2 else \
      address if mode == 1 else self.mem[address]

  def adjust_relative(self, m1):
    """ Adjusts the relative base by the value of its only parameter
    """
    v1 = self.get_value(self.ptr + 1, m1)
    self.logger.info("Adjust rel ptr from {} to {}". \
      format(self.relative, self.relative + v1))
    self.relative += v1
    self.ptr += 2

  def equals(self, m1, m2, m3):
    """ If the first parameter is equal to the second parameter, 
        it stores 1 in the position given by the third parameter.
        Otherwise, it stores 0.
    """
    v1 = self.get_value(self.ptr + 1, m1)
    v2 = self.get_value(self.ptr + 2, m2)
    target_pos = self.get_position(self.ptr + 3, m3)
    self.logger.info("Equals {} == {} = {}, {} -> [{}]". \
      format(v1, v2, v1 == v2, 1 if v1 == v2 else 0, target_pos))
    self.mem[target_pos] = 1 if v1 == v2 else 0
    self.ptr += 4

  def less_than(self, m1, m2, m3):
    """ If the first parameter is less than the second parameter,
        it stores 1 in the position given by the third parameter.
        Otherwise, it stores 0.
    """
    v1 = self.get_value(self.ptr + 1, m1)
    v2 = self.get_value(self.ptr + 2, m2)
    target_pos = self.get_position(self.ptr + 3, m3)
    self.logger.info("LessThan {} < {} = {}, {} -> [{}]". \
      format(v1, v2, v1 < v2, 1 if v1 < v2 else 0, target_pos))
    self.mem[target_pos] = 1 if v1 < v2 else 0
    self.ptr += 4

  def jump_if_true(self, m1, m2):
    """ If the first parameter is non-zero, it sets the instruction pointer
        to the value from the second parameter.
        Otherwise, it does nothing
    """
    v1 = self.get_value(self.ptr + 1, m1)
    v2 = self.get_value(self.ptr + 2, m2)
    test = v1 != 0
    if test == True:
      self.logger.info("JumpIfTrue -> [{}]".format(v2))
      self.ptr = v2
    else:
      self.logger.info("JumpIfTrue -".format(v2))
      self.ptr += 3

  def jump_if_false(self, m1, m2):
    """ If the first parameter is zero, it sets the instruction pointer 
        to the value from the second parameter.
        Otherwise, it does nothing
    """
    v1 = self.get_value(self.ptr + 1, m1)
    v2 = self.get_value(self.ptr + 2, m2)
    test = v1 != 0
    if test == False:
      self.logger.info("JumpIfFalse -> [{}]".format(v2))
      self.ptr = v2
    else:
      self.logger.info("JumpIfTrue -".format(v2))
      self.ptr += 3

  def read(self, mode):
    """ Takes a single integer as input and saves it 
        to the position given by its only parameter
    """
    target_pos = self.get_position(self.ptr + 1, mode)
    """ If stdin is empty, we stop processing instructions 
        (simulating a wait for stdin).
        Program must be started again from external.
        Hope this is sufficient :)
    """
    if not self.stdin:
      return False

    value = self.stdin.pop(0)
    self.logger.info("Read: stdin {} -> [{}]".format(value, target_pos))
    self.mem[target_pos] = value
    self.ptr += 2
    return True

  def write(self, mode):
    """ Outputs the value of its only parameter
    """
    value = self.get_value(self.ptr + 1, mode)
    self.logger.info("Write [{}] to stdout".format(value))
    self.stdout.append(value)
    self.ptr += 2

  def add(self, m1, m2, m3):
    """ Performs an addition operation
    """
    p1 = self.get_value(self.ptr + 1, m1)
    p2 = self.get_value(self.ptr + 2, m2)
    pr = self.get_position(self.ptr + 3, m3)
    self.logger.info("arithmetic plus: {} + {} = {} -> [{}]". \
      format(p1, p2, p1 + p2, pr))
    self.mem[pr] = p1 + p2
    self.ptr += 4

  def mul(self, m1, m2, m3):
    """ Performs an multplication operation
    """
    p1 = self.get_value(self.ptr + 1, m1)
    p2 = self.get_value(self.ptr + 2, m2)
    pr = self.get_position(self.ptr + 3, m3)
    self.logger.info("arithmetic plus: {} * {} = {} -> [{}]". \
      format(p1, p2, p1 * p2, pr))
    self.mem[pr] = p1 * p2
    self.ptr += 4

  def get(self, position):
    """ Returns the memory content on the specified position
    """
    return self.mem[position]

  def patch(self, position, value):
    """ Update the memory content on the specified position
        by the specified value.
        First used on day 2.
    """
    self.mem[position] = value

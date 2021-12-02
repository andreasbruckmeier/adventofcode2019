#!/usr/bin/env python3
import logging
import sys
import os
import icc
import readchar
import time

class ArcadeGame():

  def __init__(self, code):

    self.computer = icc.IntCodeComputer()
    self.computer.load(code)
    self.computer.patch(0, 2) # hack a free game :)
    self.dimension = [39,23] # determined during tests, could be coded as well
    self.game = [[0 for y in range(self.dimension[1] + 1)] \
                    for x in range(self.dimension[0] + 1)]
    self.score = 0
    # 0:space, 1:wall, 2:block, 3:paddle, 4:ball
    self.elements = {0: ' ', 1: '\u2588', 2: '\u25A2', 3: '\u25AC', 4: '\u25C9'}

  def parse_output(self):

    state = 0
    score = None
    x = 0
    y = 0
    while True:
      output = self.computer.read_stdout()
      if output == None:
        break
      if state == 0:
        x = output
      elif state == 1:
        y = output
      elif state == 2:
        if x == -1 and y == 0:
          self.score = output
        else:
          self.game[x][y] = output
          if output == 4:
            self.ball = (x,y)
          elif output == 3:
            self.paddle = (x,y)
      state = (state + 1) % 3

  def draw(self):

    os.system('clear')
    print()
    for y in range(self.dimension[1] + 1):
      print("\n    ", end='')
      for x in range(self.dimension[0] + 1):
        print(self.elements[self.game[x][y]], end='')


  def evaluate(self):

    return self.ball[0] - self.paddle[0]

  def play(self):

    evaluation = 0
    frame = 0

    while True:
      self.computer.put_stdin(evaluation)
      self.computer.run()
      if self.computer.halted:
        self.parse_output()
        self.draw()
        print("\n\n    GAME OVER\n    FINAL SCORE:", self.score)
      self.parse_output()
      evaluation = self.evaluate()
      if frame % 1 == 0:
        self.draw()
        print("\n\n    SCORE:", self.score)
      frame += 1
      time.sleep(0.1)

if __name__ == "__main__":

  loglevel = 'WARNING'
  logger = logging.getLogger()
  logger.disabled = True # toggle to log something
  logger.setLevel(getattr(logging, loglevel))
  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(getattr(logging, loglevel))
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  game = ArcadeGame('input.txt')
  game.play()

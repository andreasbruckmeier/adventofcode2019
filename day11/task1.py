#!/usr/bin/env python3
import logging
import sys
import icc

class EmergencyHullPaintingRobot:

  def __init__(self):

    self.position = (0,0)
    self.direction = (0,1)
    self.visited_panels = {}

  def __repr__(self):

    return '<' + str(self.position) + ',' + str(self.direction) + '>'

  def rotate(self, direction):
    """ 0 clockwise, 1 counterclockwise """
    rotate_cw = {
      (0,1): (1,0),
      (1,0): (0,-1),
      (0,-1): (-1,0),
      (-1,0): (0,1)
    }

    rotate_ccw = {
      (0,1): (-1,0),
      (-1,0): (0,-1),
      (0,-1): (1,0),
      (1,0): (0,1)
    }

    if direction == 0:
      self.direction = rotate_cw[self.direction]
    else:
      self.direction = rotate_ccw[self.direction]

  def move(self):
    """ Moves the robot one panel in self.direction """
    self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

  def paint(self, color):
    """ color: 0 black, 1 white """
    if self.position in self.visited_panels:
      self.visited_panels[self.position] = (color, self.visited_panels[self.position][1] + 1)
    else:
      self.visited_panels[self.position] = (color, 1)

  def  get_color(self):
    """ Returns the color of an already visited panel or zero if unvisited """
    if self.position in self.visited_panels:
      return self.visited_panels[self.position][0]
    return 0

if __name__ == "__main__":

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
  icc.load(code)

  robot = EmergencyHullPaintingRobot()

  # robot was expecting to start on a white panel, not a black one
  icc.put_stdin(1)

  # run program until halted
  while True:
    icc.run()
    if icc.halted:
      break
    robot.paint(icc.read_stdout())
    robot.rotate(icc.read_stdout())
    robot.move()
    icc.put_stdin(robot.get_color())

  max_x = 0
  min_x = 0
  max_y = 0
  min_y = 0
  for i in robot.visited_panels:
    max_x = i[0] if i[0] > max_x else max_x
    max_y = i[1] if i[1] > max_y else max_y
    min_x = i[0] if i[0] < min_x else min_x
    min_y = i[1] if i[1] < min_y else min_y

  print(max_x, max_y, min_x, min_y)

  # This reveals that the robot does not move into negative coordinates
  # Unfortunately because of my choice all coordinates get negative
  # But this is no problem, I just print negativ coordinates :)

  for y in range(0, -6, -1):
    for x in range(0, -43, -1):
      if (x,y) in robot.visited_panels:
        print('#' if robot.visited_panels[(x,y)][0] else ' ', end='')
      else:
        print('-', end='')
    print()

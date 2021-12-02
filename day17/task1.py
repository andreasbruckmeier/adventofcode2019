import logging
import sys
import icc

# direction vectors used to look around a location
direction_r = [-1,0,1,0]
direction_c = [0,1,0,-1]

def draw(space):

  for row in range(len(space)):
    for col in range(len(space[0])):
      print('.' if space[row][col] in [0,46] else '#' if space[row][col] in [1,35] else chr(space[row][col]), end='')
    print()

def build_map(space):

  rows = 0
  cols = 0

  robot = None

  com = icc.IntCodeComputer()
  com.load('input.txt')
  com.run()

  line = []
  point = com.read_stdout()
  current_col = 0
  while point:
    if point == 10:
      if line:
        space.append(line)
        line = []
        rows += 1
        current_col = 0
      else:
        break
    else:
      # robot
      if point in [118,94,60,62]:
        robot = (rows, current_col)
      line.append(point)
      current_col += 1
      cols = current_col
    point = com.read_stdout()

  return rows, cols, robot

def discover_scaffold(space, robot, cols, rows):
  #breakpoint()
  visited = [[0 for x in range(cols)] for y in range(rows)] 
  visited[robot[0]][robot[1]] = 1
  intersections = []

  robot_move_list = []

  # direction in which robot is facing
  # 94 up , 62 right, 118 down, 60 left
  robot_char = space[robot[0]][robot[1]]
  robot_facing = (-1,0) if robot_char == 94 else (0,1) if robot_char == 62 \
                  else (1,0) if robot_char == 118 else (0,-1)

  # determine starting direction from robots facing direction
  cur_direction = direction_r.index(robot_facing[0])

  while True:

    move_found = False

    # check neighbours
    for i in range(cur_direction, cur_direction + 4):

      #if robot == (28, 0):
      #  breakpoint()

      i_mod = i % 4
      cur_direction_mod = cur_direction % 4

      checked_pos = (robot[0] + direction_r[i_mod], robot[1] + direction_c[i_mod])

      # check out of bounds
      if checked_pos[0] >= rows or checked_pos[1] >= cols \
        or checked_pos[0] < 0 or checked_pos[1] < 0:
        continue

      checked_value = space[checked_pos[0]][checked_pos[1]]

      if checked_value == 35:

        # prevent running backwards
        if direction_r[i_mod] == -direction_r[cur_direction_mod] and \
          direction_c[i_mod] == -direction_c[cur_direction_mod] and \
          visited[checked_pos[0]][checked_pos[1]]:
          continue

        move_found = True

        # detect and store direction change
        if cur_direction != i:
          if (cur_direction_mod, i_mod) in [(0,3), (3,2), (2,1), (1,0)]:
            rotation = 'L'
          else:
            rotation = 'R'
          robot_move_list.append(rotation)

        # count move in move list
        if type(robot_move_list[-1]) != int:
          robot_move_list.append(1)
        else:
          robot_move_list[-1] += 1

        cur_direction = i

        if visited[checked_pos[0]][checked_pos[1]]:
          intersections.append((checked_pos[0], checked_pos[1]))
        else:
          visited[checked_pos[0]][checked_pos[1]] = 1

        robot = (checked_pos[0], checked_pos[1])
        break

    if not move_found:
      return intersections, robot_move_list

  return None

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

  space = []

  # build space map from input file
  rows, cols, robot = build_map(space)

  # walk along scaffold and collect information
  intersections, robot_move_list = discover_scaffold(space, robot, cols, rows)

  # give solution for task 1
  print("Task 1 - sum of the alignment parameters:", sum([x[0] * x[1] for x in intersections]))

  # task 2
  #draw(space)
  func_a = "L,8,R,10,L,10\n"
  func_b = "R,10,L,8,L,8,L,10\n"
  func_c = "L,4,L,6,L,8,L,8\n"
  main_routine = "A,B,A,C,B,C,A,C,B,C\n"

  com = icc.IntCodeComputer()
  com.load('input.txt')

  """ Force the vacuum robot to wake up by changing the value 
      in your ASCII program at address 0 from 1 to 2. """
  com.patch(0,2)
  com.run()

  # assert main prompt
  assert ''.join(map(chr, com.read_stdout(True)))[-6:] == "Main:\n"

  # input main routine and run
  for char in main_routine:
    com.put_stdin(ord(char))
  com.run()

  # assert func A prompt
  assert ''.join(map(chr, com.read_stdout(True)))[-12:] == "Function A:\n"

  # input func A and run
  for char in func_a:
    com.put_stdin(ord(char))
  com.run()

  # assert func B prompt
  assert ''.join(map(chr, com.read_stdout(True)))[-12:] == "Function B:\n"

  # input func B and run
  for char in func_b:
    com.put_stdin(ord(char))
  com.run()

  # assert func C prompt
  assert ''.join(map(chr, com.read_stdout(True)))[-12:] == "Function C:\n"

  # input func C and run
  for char in func_c:
    com.put_stdin(ord(char))
  com.run()

  # assert video feed prompt
  assert ''.join(map(chr, com.read_stdout(True)))[-23:] == "Continuous video feed?\n"

  # input func C and run
  for char in "n\n":
    com.put_stdin(ord(char))
  com.run()

  print("Task 2 - collected space dust:", com.read_stdout(True)[-1])

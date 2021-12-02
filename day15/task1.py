from collections import deque
import icc
import time

class BreadthFirstSearch:
  """
  After several unsuccesful tries using recursive backtracking or 
  other approaches, I finally searched for algorithms to scan 
  unknown grids with obstacles. This lead to some graph theory algorithms
  and in the end to the "Breadth First Search" which can be used to solve
  labyrinth puzzles.

  The breakthrough came with this video:
  https://www.youtube.com/watch?v=KiCBXu4P-2Y

  Breadth First Search can be used to find the shortest path in a graph if
  - There are no loops
  - All edges have same weight or no weight
  All conditions are given in the context of a labyrinth.

  This AoC task is a little bit more complex as you have no grid to work on.
  You need to explore the grid while running the algorithm,
  which is a bit tricky using the IntCodeComputer :)

  Drawing the explored area was super fun in the end!
  """
  def __init__(self, starting_point = (0,0)):

    self.starting_point = starting_point # starting point

    # queue and visited list used by 'Breadth First Search'
    self.queue = deque()
    self.visited = []

    # keeps track on how to move the robot to a specific location
    self.robot_move_list = {
      starting_point: []
    }

    self.reached_end = False
    self.stop_at_end = True # for task 2 to explore the whole area

    # n,s,w,e direction vectors
    self.direction_x = [0,0,-1,1]
    self.direction_y = [1,-1,0,0]

    self.oxygen_system = None

  def draw_area(self):
    """ Draws the labyrinth to stdout
    """
    moves_to_target = self.translate_moves_to_coordinates(self.oxygen_system)

    extremata = [0,0,0,0]

    # determine grid dimensions from visited locations
    for i in self.visited:
      if i[0] > extremata[0]:
        extremata[0] = i[0]
      elif i[0] < extremata[1]:
        extremata[1] = i[0]
      if i[1] > extremata[2]:
        extremata[2] = i[1]
      elif i[1] < extremata[3]:
        extremata[3] = i[1]

    # actual drawing
    for y in range(extremata[2] + 1, extremata[3] - 2, -1):
      for x in range(extremata[1] - 1, extremata[0] + 2):
        if (x,y) in self.visited:
          if (x,y) == self.starting_point:
            print('\033[31m' + 'S' + '\033[0m', end='')
          elif (x,y) == self.oxygen_system:
            print('\033[31m' + 'O' + '\033[0m', end='')
          elif (x,y) in moves_to_target:
            print('\033[32m' + '.' + '\033[0m', end='')
          else:
            print(' ', end='')
        else:
          print('\u2588', end='')
      print()

  def translate_moves_to_coordinates(self, position):
    """ Follow the speficied move list entry to the end and translate
        all move instructions to absolute coordinates
    """
    coordinate = self.starting_point
    coordinates = []
    for i in self.robot_move_list[position]:
      coordinate = (coordinate[0] + self.direction_x[i-1], coordinate[1] + self.direction_y[i-1])
      coordinates.append(coordinate)
    return coordinates

  def get_computer_at_position(self, position):
    """ Returns a new IntcodeComputer instance wich is moved
        to the specified position in the grid
    """
    com = icc.IntCodeComputer()
    com.load('input.txt')
    # this should never happen
    assert position in self.robot_move_list
    for move in self.robot_move_list[position]:
      com.put_stdin(move)
    com.run()
    # if specified position is the starting point, 
    # there are no moves and there is no output, so we simulate one with 1
    output = 1 if not com.stdout else com.stdout[-1]
    com.stdout = []
    return com, output

  def explore_neighbours(self, computer, position):

    # loop over current positions neighbours (n,s,w,e)
    for i in range(4):

      new_position = (position[0] + self.direction_x[i], position[1] + self.direction_y[i])

      # skip neighbour if already visited 
      if new_position in self.visited:
        continue

      # move robot to current neighbour (robots move directions start at 1!)
      computer.put_stdin(i + 1)
      computer.run()
      out = computer.read_stdout()

      # This neighbour is a wall, skip it
      if out == 0:
        continue

      # Check edge case where two ore more paths can reach this neighbour
      # Fortunately this is not the case for my input :)
      assert new_position not in self.robot_move_list

      # Add this neighbour to the robot move list
      self.robot_move_list[new_position] = self.robot_move_list[position] + [i + 1]

      # Move robot back from this neighbour to its initial position
      if i == 0:
        computer.put_stdin(2)
      elif i == 1:
        computer.put_stdin(1)
      elif i == 2:
        computer.put_stdin(4)
      elif i == 3:
        computer.put_stdin(3)

      computer.run()

      # We should never ever hit a wall when returning from a neighbour
      assert computer.read_stdout() in [1,2]

      self.queue.append(new_position)
      self.visited.append(new_position)

  def solve(self):
    """ Main method of the 'Breadth First Search' algorithm
    """
    self.queue.append(self.starting_point)
    self.visited.append(self.starting_point)

    # If the queue is empty. there is nothing left to explore 
    while len(self.queue) > 0:

      current = self.queue.pop()

      # Get a new Intcode Computer at the current position
      # -> Super bad performance but it works :)
      com, output = self.get_computer_at_position(current)

      # Test if we reached the oxygen system
      if output == 2:
        self.reached_end = True
        self.oxygen_system = current
        if self.stop_at_end: # condition for task2
          break

      # Explore neighbours
      self.explore_neighbours(com, current)

    if self.reached_end:
      return len(bfs.robot_move_list[bfs.oxygen_system])

    return -1

"""
Task 1
"""
bfs = BreadthFirstSearch()
print("Task 1:\nShortest path to oxygen system: {}".format(bfs.solve()))
#bfs.draw_area()

"""
Task 2

For task 2 we set the oxygen system as starting point and search all fields.
Finally we use the longest move list minus the number of moves from the
robot start point to the oxygen system as solution for task 2.
"""
start = bfs.oxygen_system
bfs2 = BreadthFirstSearch(start)
bfs2.robot_move_list = {
  start: bfs.robot_move_list[bfs.oxygen_system]
}
bfs2.stop_at_end = False
bfs2.solve()
time_to_fill = max([len(x) for x in bfs2.robot_move_list.values()]) \
                - len(bfs2.robot_move_list[start])
print("Task 2:\nTime to fill the whole area with oxygen: {}".format(time_to_fill))
#bfs2.draw_area()

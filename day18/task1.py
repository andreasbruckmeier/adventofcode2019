from collections import deque
from os import system
import icc
import time

class ObjectNode:

  def __init__(self, position, previous = None):

    self.row = position[0]
    self.col = position[1]
    self.previous = previous
    self.previous_distance = None
    self.next = []
    self.key = None
    self.door = None

  def __eq__(self, other): 
    if not isinstance(other, ObjectNode):
      return NotImplemented
    return self.row == other.row and self.col == other.col

  def __str__(self):

    return '<({},{})>'.format(self.row, self.col) + (' key {}'.format(self.key) if self.key else ' door {}'.format(self.door) if self.door else '')

  def get_next_obects(self):

    nodes = []

    for node in self.next:
      if node.key or node.door:
        nodes.append((1,node))
      else:
        n = node.get_next_obects()
        for i in n:
          nodes.append((i[0]+1, i[1]))

    return nodes

class Vault:

  WALL = '\u2588'
  FLOOR = ' '
  ENTRANCE = '@'

  def __init__(self, input_file):

    self.vault = []
    self.nodes = {}

    with open(input_file, 'r') as f:
      for line in f.readlines():
        self.vault.append([tile for tile in line.strip().replace('.', self.FLOOR).replace('#', self.WALL)])

    # dimensions of vault
    self.rows = len(self.vault)
    self.cols = len(self.vault[0])

    # coordinates of entrance
    self.entrance = (self.vault.index([x for x in self.vault if '@' in x][0]),\
                      [x for x in self.vault if '@' in x][0].index('@'))

    self.queue = deque()
    self.visited = []

    self.move_count = 0
    self.nodes_left_in_layer = 1
    self.nodes_in_next_layer = 0

    # n,s,w,e direction vectors
    self.direction_row = [-1, 1, 0, 0]
    self.direction_col = [0, 0, -1, 1]

  def draw(self):

    system('clear')
    for row in range(self.rows):
      for col in range(self.cols):
        print(self.vault[row][col], end='')
      print()

  def explore_neighbours(self, node):

    # loop over current positions neighbours (n,s,w,e)
    for i in range(4):

      new_node = ObjectNode((node.row + self.direction_row[i], node.col + self.direction_col[i]), node)

      # skip neighbour if already visited 
      if new_node in self.visited:
        continue

      new_position_tile = self.vault[new_node.row][new_node.col]

      # This neighbour is a wall, skip it
      if new_position_tile == self.WALL:
        continue

      self.queue.append(new_node)
      self.visited.append(new_node)
      self.nodes_in_next_layer += 1

  def solve(self):
    """ Main method of the 'Breadth First Search' algorithm
    """
    start_node = ObjectNode(self.entrance)
    self.queue.append(start_node)
    self.visited.append(start_node)

    # If the queue is empty. there is nothing left to explore 
    while len(self.queue) > 0:

      current = self.queue.popleft()

      # set me as next of previous if it exists
      if current.previous:
        current.previous.next.append(current)

      current_tile = self.vault[current.row][current.col]

      # fancy drawing of progress
      #self.vault[current.row][current.col] = '\033[32m' + 'x' + '\033[0m'
      #self.draw()
      #time.sleep(.03)

      # key or door
      if current_tile not in [self.FLOOR, self.ENTRANCE]:
        if current_tile.isupper():
          current.door = current_tile
        else:
          current.key = current_tile

      # Explore neighbours
      self.explore_neighbours(current)

      self.nodes_left_in_layer -= 1

      if self.nodes_left_in_layer == 0:
        self.nodes_left_in_layer = self.nodes_in_next_layer
        self.nodes_in_next_layer = 0
        self.move_count += 1

    return -1

def clean_graph(current_node):

  next_nodes = []

  for node in current_node.get_next_obects():
    node[1].previous_distance = node[0]
    node[1].previous = current_node
    next_nodes.append(node[1])
    clean_graph(node[1])

  current_node.next = next_nodes

def dive(node, dive_list, chain = []):

  for child in node.next:
    dive(child, dive_list, chain + [child])
  dive_list.append(chain)


if __name__ == "__main__":

  vault = Vault('input.txt')
  vault.solve()

  clean_graph(vault.visited[0])

  dive_list = []

  dive(vault.visited[0], dive_list)

  for i in sorted(dive_list, key=lambda x: len(x)):
    print(i)
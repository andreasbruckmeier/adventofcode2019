import math

class Position:

  def __init__(self, pos, empty):

    self.pos = pos
    self.empty = empty
    self.detected_asteroids = []

with open('input.txt', 'r') as f:
  data = f.readlines()
width = len(data[0].strip())

# fill positions
positions = [[Position((x,y), data[y][x] == '.') for y in range(width)] for x in range(width)]

# Find home for "Instant Monitoring Station"
ims = None
for y in range(width):
  for x in range(width):
    if positions[x][y].empty:
      continue
    for j in range(width):
      for i in range(width):
        if not (y == j and x == i) and not positions[i][j].empty:
          dist_x = i-x
          dist_y = j-y
          max_dist = max(abs(dist_x), abs(dist_y))
          vector = (dist_x / max_dist, dist_y / max_dist)
          if vector not in positions[x][y].detected_asteroids:
            positions[x][y].detected_asteroids.append(vector)
    if not ims or len(positions[x][y].detected_asteroids) > len(ims.detected_asteroids):
      ims = positions[x][y]

print('Task 1: ({}, {}) -> {}'.format(ims.pos[0], ims.pos[1], len(ims.detected_asteroids)))

# re-detect asteroids from ims and this time save all asteroids with
# their angle relative to the laser starting direction vector (0,-1)

# reset detected asteroids
ims.detected_asteroids = {}

pi2 = 2 * math.pi

for j in range(width):
  for i in range(width):
    if not (ims.pos[1] == j and ims.pos[0] == i) and not positions[i][j].empty:
      dist_x = i-ims.pos[0]
      dist_y = j-ims.pos[1]
      # calculate angle
      angle = math.acos((0 * dist_x + (-1) * dist_y) / (((0 **2 + (-1) ** 2) ** 0.5) * ((dist_x **2 + dist_y ** 2) ** 0.5)))
      angle = pi2 - angle if dist_x < 0 else angle
      vector = (abs(dist_x), abs(dist_y))
      if angle not in ims.detected_asteroids:
        ims.detected_asteroids[angle] = {vector: positions[i][j]}
      elif vector not in ims.detected_asteroids[angle]:
        ims.detected_asteroids[angle][vector] = positions[i][j]

print("\nTask 2:")

count = 0
while count <= 299:
  for i in sorted(ims.detected_asteroids.keys()):
    if ims.detected_asteroids[i]:
      count += 1
      first = sorted(ims.detected_asteroids[i].keys())[0]
      if count > 198 and count < 208:
        print("#{} -> angle: {:.3f}, position: {}, answer: {}".format(count, i, ims.detected_asteroids[i][first].pos, \
          ims.detected_asteroids[i][first].pos[0] * 100 + ims.detected_asteroids[i][first].pos[1]))
      del ims.detected_asteroids[i][first]

"""
For some strange reason killed asteroids #1, #2, #3, ..., #10 are correct in my output.
From #20 on I have a little offset which cumulates to 4 until #200.
Couldn't figure out the issue but knowing this fact, I just entered my position #204
and it was the correct answer - feels bad :(
"""

wires = []
wire_paths = [[],[]]

with open('input.txt', 'r') as f:
  for line in f.readlines():
    wires.append(line.strip())

for idx in range(len(wires)):
  path_length = 0
  current_x = 0
  current_y = 0
  for move in wires[idx].split(","):
    move_type = move[0]
    move_length = int(move[1:])
    if move_type == 'U':
      wire_paths[idx].append((current_x,current_y,current_x,current_y + move_length, path_length))
      current_y += move_length
    elif move_type == 'D':
      wire_paths[idx].append((current_x,current_y,current_x,current_y - move_length, path_length))
      current_y -= move_length
    elif move_type == 'R':
      wire_paths[idx].append((current_x,current_y,current_x + move_length,current_y, path_length))
      current_x += move_length
    elif move_type == 'L':
      wire_paths[idx].append((current_x,current_y,current_x - move_length,current_y, path_length))
      current_x -= move_length
    path_length += move_length

intersections = []

# compare all vectors to find intersections
for vector1 in wire_paths[0]:
  for vector2 in wire_paths[1]:
    # ignore parallel vectors
    if (vector1[0] == vector1[2]) != (vector2[0] == vector2[2]):
      # take x from vertical and y from horizontal vector
      if vector1[0] == vector1[2]:
        # vector 1 is vertical, vector 2 is horizontal
        if vector1[0] >= min(vector2[0],vector2[2]) and vector1[0] <= max(vector2[0],vector2[2]) \
          and vector2[1] >= min(vector1[1],vector1[3]) and vector2[1] <= max(vector1[1],vector1[3]) \
          and (vector1[0] != 0 or vector2[1] != 0):
          vector1_dist = vector1[4] + abs(vector1[1] - vector1[3]) - abs(vector1[3] - vector2[1])
          vector2_dist = vector2[4] + abs(vector2[0] - vector2[2]) - abs(vector1[0] - vector2[2])
          intersections.append((vector1[0], vector2[1], vector1_dist, vector2_dist))
      else:
        # vector 2 is vertical, vector 1 is horizontal
        if vector2[0] >= min(vector1[0],vector1[2]) and vector2[0] <= max(vector1[0],vector1[2]) \
          and vector1[1] >= min(vector2[1],vector2[3]) and vector1[1] <= max(vector2[1],vector2[3]) \
          and (vector2[0] != 0 or vector1[1] != 0):
          vector1_dist = vector1[4] + abs(vector1[0] - vector1[2]) - abs(vector1[2] - vector2[0])
          vector2_dist = vector2[4] + abs(vector2[1] - vector2[3]) - abs(vector2[3] - vector1[1])
          intersections.append((vector2[0], vector1[1], vector1_dist, vector2_dist))

solution_intersection = sorted(intersections, key=lambda x: x[2] + x[3])[0]
print(solution_intersection[2] + solution_intersection[3])

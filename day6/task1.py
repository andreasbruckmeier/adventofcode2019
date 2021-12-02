class Object:

  def __init__(self, name):
    self.name = name
    self.orbiting_objects = []

  def __str__(self):
    return self.name

  def __repr__(self):
    return '<' + self.name + ':' + ','.join(map(str, self.orbiting_objects)) + '>'

  def add_orbiting_object(self, object):
    if object not in self.orbiting_objects:
      self.orbiting_objects.append(object)

  def count_direct_orbiting_objects(self):
    return len(self.orbiting_objects)

  def get_orbiting_objects(self):
    return (i for i in self.orbiting_objects)


objects = {}

with open('input.txt', 'r') as f:
  for line in f.readlines():
    obj_name1, obj_name2 = line.strip().split(")")
    if obj_name1 in objects:
      obj1 = objects[obj_name1]
    else:
      objects[obj_name1] = obj1 = Object(obj_name1)
    if obj_name2 in objects:
      obj2 = objects[obj_name2]
    else:
      objects[obj_name2] = obj2 = Object(obj_name2)
    obj1.add_orbiting_object(obj2)

def generate_paths(object, path = []):
  if object.count_direct_orbiting_objects() == 0:
    yield path + [object]
  for subobj in object.get_orbiting_objects():
    yield from generate_paths(subobj, path + [object])

paths = list(generate_paths(objects['COM']))

orbits = {}

for path in paths:
  for i in path:
    for j in path:
      if i == j:
        continue
      orb = str(i) + "-" + str(j)
      rev_orb = str(j) + "-" + str(i)
      if orb not in orbits and rev_orb not in orbits:
        orbits[orb] = 1

print(len(orbits))

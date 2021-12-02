from itertools import combinations
import math
import re

class Moon:

  def __init__(self, position):

    self.position = position
    self.velocity = (0,0,0)
    self.next_velocity = None

  def __repr__(self):

    return '<{},{}>'.format(self.position, self.velocity)

  def calculate_next_velocity(self, moon):

    self.next_velocity = (
      self.next_velocity[0] + 1 if self.position[0] < moon.position[0] \
        else self.next_velocity[0] - 1 if self.position[0] > moon.position[0] \
        else self.next_velocity[0],
      self.next_velocity[1] + 1 if self.position[1] < moon.position[1] \
        else self.next_velocity[1] - 1 if self.position[1] > moon.position[1] \
        else self.next_velocity[1],
      self.next_velocity[2] + 1 if self.position[2] < moon.position[2] \
        else self.next_velocity[2] - 1 if self.position[2] > moon.position[2] \
        else self.next_velocity[2]
    )

  def apply_velocity(self):

    self.position = (
      self.position[0] + self.velocity[0],
      self.position[1] + self.velocity[1],
      self.position[2] + self.velocity[2]
    )

  def get_potential_energy(self):

    return abs(self.position[0]) + abs(self.position[1]) + abs(self.position[2])

  def get_kinetic_energy(self):

    return abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])


if __name__ == "__main__":

  first_state = [None for x in range(3)]
  cycles = [None for x in range(3)]

  moon_regex = re.compile('^<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>$')
  moons = []

  with open('input.txt', 'r') as f:
    for line in f.readlines():
      match = moon_regex.match(line)
      moons.append(Moon((int(match.group(1)), int(match.group(2)), int(match.group(3)))))

  step = 1
  while True:

    # clone current velocity
    for i in moons:
      i.next_velocity = i.velocity

    # calculate new velocity for each moon
    for i,j in combinations(range(len(moons)), 2):
      moons[i].calculate_next_velocity(moons[j])
      moons[j].calculate_next_velocity(moons[i])

    # set new velocity for each moon
    total_energy = 0
    for i in moons:
      i.velocity = i.next_velocity
      i.apply_velocity()
      total_energy += i.get_potential_energy() * i.get_kinetic_energy()

    if step == 1000:
      print("Task 1: Total energy after step 1000 =", total_energy)

    for i in range(3):
      if first_state[i] == None:
        first_state[i] = '-'.join([str(x.position[i]) + '-' + str(x.velocity[i]) for x in moons])
      elif first_state[i] == '-'.join([str(x.position[i]) + '-' + str(x.velocity[i]) for x in moons]):
        cycles[i] = step - 1
        first_state[i] = False

    if all(cycles):
      break

    step += 1

def lcm(c):
  lcm = c[0]
  for i in c[1:]:
    lcm = lcm*i//math.gcd(lcm, i)
  return lcm

print("Task 2: Universe repeats after", lcm(cycles), "steps")

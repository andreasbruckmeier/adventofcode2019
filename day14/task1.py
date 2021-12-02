import copy

def calculate(reactions, factor = 1):

  fuel = {k: v*factor for k, v in reactions['FUEL'][1].items()}
  del reactions['FUEL']

  while True:

    suplement_counter = 0

    for substituted in list(fuel.keys()):

      if substituted == 'ORE':
        continue

      # check if subsituted only appear on right side
      if len([l[1] for k,l in reactions.items() if substituted in l[1].keys()]) > 0:
        continue

      substitute_batch_size = reactions[substituted][0]
      substituted_quantity = fuel[substituted]

      if substitute_batch_size >= substituted_quantity:
        factor = 1
      elif substituted_quantity % substitute_batch_size == 0:
        factor = substituted_quantity // substitute_batch_size
      else:
        factor = substituted_quantity // substitute_batch_size + 1

      for replacement in reactions[substituted][1]:

        if replacement not in fuel:
          fuel[replacement] = factor * reactions[substituted][1][replacement]
        else:
          fuel[replacement] += factor * reactions[substituted][1][replacement]

      del fuel[substituted]
      del reactions[substituted]

      suplement_counter += 1

    if suplement_counter == 0:
      break

  return fuel['ORE']

def binsearch(reactions, high, target):
  low = 1
  while low < high:
    mid = (low+high) // 2
    midval = calculate(copy.deepcopy(reactions), mid)
    if midval < target:
        low = mid+1
    elif midval > target: 
        high = mid
    else:
        return mid
  return mid - 1 if midval > target else mid

reactions = {}

with open('input.txt', 'r') as f:
  for line in f.readlines():
    inputs, output = line.strip().split(' => ')
    inputs = [[int(x.split(" ")[0]), x.split(" ")[1]] for x in inputs.split(", ")]
    output = [int(output.split(" ")[0]), output.split(" ")[1]]
    reactions[output[1]] = [output[0] ,{}]
    for i in inputs:
      reactions[output[1]][1][i[1]] = i[0]

print("Task 1:", calculate(copy.deepcopy(reactions)))

# solution for task is quick enough to just 
# try out some values in binary search style
print("Task 2:", binsearch(reactions, 1000000000000, 1000000000000))

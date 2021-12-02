with open('input.txt', 'r') as f:
  total_fuel_requirement = 0
  for module in map(int, f):
    total_fuel_requirement += module // 3 - 2
  print(total_fuel_requirement)

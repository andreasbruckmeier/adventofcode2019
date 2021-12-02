with open('input.txt', 'r') as f:
  total_fuel_requirement = 0
  for module in map(int, f):
    fuel_requirement = module // 3 - 2
    total_fuel_requirement += fuel_requirement
    while True:
      fuel_requirement = fuel_requirement // 3 - 2
      if fuel_requirement >= 0:
        total_fuel_requirement += fuel_requirement
      else:
        break

print(total_fuel_requirement)

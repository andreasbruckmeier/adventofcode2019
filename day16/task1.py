BASE_PATTERN = [0, 1, 0, -1]

# pattern generator for current position
def get_pattern(position):

  skip = True
  while True:
    for i in BASE_PATTERN:
      for j in range(position + 1):
        if skip:
          skip = False
          continue
        yield i

def run_phase(input):

  result = []
  # loop over length of input (=> positions in input)
  for position in range(len(input)):
    pattern = get_pattern(position)
    value = 0
    # loop over input char by char
    for x in [x for x in input]:
      value += int(x) * next(pattern)
    # Then, only the ones digit is kept: 38 becomes 8, -17 becomes 7, and so on
    result.append(str(abs(value)%10))
  return ''.join(result)

with open('input.txt', 'r') as file:
  input = file.read().replace('\n', '')

# task 1
for phase in range(100):
  input = run_phase(input)

print("First eight digits after phase{} are {}".format(phase + 1, input[0:8]))

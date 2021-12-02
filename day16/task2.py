with open('input.txt', 'r') as file:
  input = file.read().replace('\n', '')

offset = int(input[0:7])
input = input * 10000
input = [int(x) for x in input.strip()[offset:]]

for phase in range(100):
  sum = 0
  new_val = []
  for i in range(len(input) - 1, -1, -1):
    sum += int(input[i])
    new_val.append(sum % 10)
  input = new_val[::-1]

print("The message is {}".format(''.join([str(x) for x in input[0:8]])))

import math

def get_prefix(password):

  length = math.floor(math.log(abs(password),10)) + 1
  prefix = 0
  tmp = 0
  for i in range(length, 0, -1):
    if tmp > (tmp := password // (10 ** (i - 1)) % 10):
      return prefix
    prefix = prefix * 10 + tmp

def has_doubles(password):

  last = -1
  while True:
    if last == (last := password % 10):
      return True
    if (password := password // 10) == 0:
      return False

def crack(password, limit, level = 0):

  length = math.floor(math.log(abs(password),10)) + 1

  if length == 6:
    if has_doubles(password):
      yield password
    return

  if level == 0:
    length_limit = math.floor(math.log(abs(limit),10)) + 1
    limit_prefix = limit // (10 ** (length_limit - length))
    for i in range(password, limit_prefix + 1):
      yield from crack(i, limit, level + 1)
  else:
    if password % 10 < password // 10 % 10:
      return
    for j in range(password % 10, 10):
      yield from crack(password * 10 + j, limit, level + 1)

  return

range_start = 372304
range_end = 847060

prefix = get_prefix(range_start)

print(len(list(crack(prefix, range_end))))

Patterns for length 4:

0 [1, 0, -1, 0]
1 [0, 1, 1, 0]
2 [0, 0, 1, 1]
3 [0, 0, 0, 1]

Patterns for length = 8:

0 [1, 0, -1, 0, 1, 0, -1, 0]
1 [0, 1, 1, 0, 0, -1, -1, 0]
2 [0, 0, 1, 1, 1, 0, 0, 0]
3 [0, 0, 0, 1, 1, 1, 1, 0]
4 [0, 0, 0, 0, 1, 1, 1, 1]
5 [0, 0, 0, 0, 0, 1, 1, 1]
6 [0, 0, 0, 0, 0, 0, 1, 1]
7 [0, 0, 0, 0, 0, 0, 0, 1]

Observations for task1:

- patterns can be stored in a map [position->pattern] to avoid re-generation of the pattern
- results for single multiplicatioins are either 0 or +/-[1-9] which can be taken directly from two lists

Observations after realizing that task 1 solution does not work for task 2 (would take ages):

- lower triangle is always 0, so it is enough to calculate the upper triangle (loop over input starting at index "position")
- lower half of patterns only consist ot 0/1 values, starting with 0s and ending with 1s
- the result for the last position in the examples is always equal to the last input digit
  -> last pattern (used for last position) results in last digit of input
  -> 2nd last pattern results in the sum of the last two digits of input mod 10 (!!!)
  -> this is valid for the lower patterns which end with a chain of 1s
- number of input digits is 650 * 10.000 => 6.500.000 (6.5 Mio x 6.5 Mio loops per phase - WTF ^^)
- offset for result is 5.972.731 (!!!) this means we can ignore the first (hard) half of the result

Prove on first example input 12345678:

0 [1, 0, -1, 0, 1, 0, -1, 0]
1 [0, 1, 1, 0, 0, -1, -1, 0]
2 [0, 0, 1, 1, 1, 0, 0, 0]
3 [0, 0, 0, 1, 1, 1, 1, 0]
4 [0, 0, 0, 0, 1, 1, 1, 1]
5 [0, 0, 0, 0, 0, 1, 1, 1]
6 [0, 0, 0, 0, 0, 0, 1, 1]
7 [0, 0, 0, 0, 0, 0, 0, 1]

- rule 7 is used to calculate 8th position:                                         1 * 8 = 8 % 10 = 8
- rule 6 is used to calculate 7th position:                                 1 * 7 + 1 * 8 = 15 % 10 = 5
- rule 5 is used to calculate 6th position:                         1 * 6 + 1 * 7 + 1 * 8 = 21 % 10 = 1
- rule 4 is used to calculate 5th position:                 1 * 5 + 1 * 6 + 1 * 7 + 1 * 8 = 26 % 10 = 6
- rule 3 is used to calculate 4th position:         1 * 4 + 1 * 5 + 1 * 6 + 1 * 7         = 22 % 10 = 2
  -> first rule where we cannot re-use the sum of the previous rule 
- rule 2 is used to calculate 3th position: 1 * 3 + 1 * 4 + 1 * 5 + 1 * 6 +               = 22 % 10 = 2
...


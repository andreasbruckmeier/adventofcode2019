import unittest

from icc.icc import IntCodeComputer

class TestSum(unittest.TestCase):

  def __init__(self, *args, **kwargs):

    self.test_data_day2 = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,6,27,2,27,13,31,1,10,31,35,1,10,35,39,2,39,6,43,1,43,5,47,2,10,47,51,1,5,51,55,1,55,13,59,1,59,9,63,2,9,63,67,1,6,67,71,1,71,13,75,1,75,10,79,1,5,79,83,1,10,83,87,1,5,87,91,1,91,9,95,2,13,95,99,1,5,99,103,2,103,9,107,1,5,107,111,2,111,9,115,1,115,6,119,2,13,119,123,1,123,5,127,1,127,9,131,1,131,10,135,1,13,135,139,2,9,139,143,1,5,143,147,1,13,147,151,1,151,2,155,1,10,155,0,99,2,14,0,0"
    super().__init__(*args, **kwargs)

  def test_day2_sample1(self):

    icc = IntCodeComputer()
    icc.load('1,0,0,0,99')
    icc.run()
    self.assertEqual(icc.dump(), [2,0,0,0,99])

  def test_day2_sample2(self):

    icc = IntCodeComputer()
    icc.load('2,3,0,3,99')
    icc.run()
    self.assertEqual(icc.dump(), [2,3,0,6,99])

  def test_day2_sample3(self):

    icc = IntCodeComputer()
    icc.load('2,4,4,5,99,0')
    icc.run()
    self.assertEqual(icc.dump(), [2,4,4,5,99])
    self.assertEqual(icc.get(5), 9801)

  def test_day2_sample4(self):

    icc = IntCodeComputer()
    icc.load('1,1,1,4,99,5,6,0,99')
    icc.run()
    self.assertEqual(icc.dump(), [30,1,1,4,2,5,6,0,99])

  def test_day2_task1(self):

    icc = IntCodeComputer()
    icc.load(self.test_data_day2)
    icc.patch(1, 12)
    icc.patch(2, 2)
    icc.run()
    self.assertEqual(icc.get(0), 4462686)

  def test_day2_task2(self):

    icc = IntCodeComputer()
    icc.load(self.test_data_day2)
    icc.patch(1, 59)
    icc.patch(2, 36)
    icc.run()
    self.assertEqual(icc.get(0), 19690720)

  def test_day5_sample1(self):
    """ Opcodes with modes """
    icc = IntCodeComputer()
    icc.load("1002,4,3,4,33")
    icc.run()
    self.assertEqual(icc.dump(), [1002, 4, 3, 4, 99])

  def test_day5_sample2(self):
    """ Negative numbers """
    icc = IntCodeComputer()
    icc.load("1101,100,-1,4,0")
    icc.run()
    self.assertEqual(icc.dump(), [1101, 100, -1, 4, 99])

  def test_equals1(self):
    icc = IntCodeComputer()
    icc.load("3,9,8,9,10,9,4,9,99,-1,8")
    icc.put_stdin(8)
    icc.run()
    self.assertEqual(icc.read_stdout(), 1)

  def test_equals2(self):
    icc = IntCodeComputer()
    icc.load("3,9,8,9,10,9,4,9,99,-1,8")
    icc.put_stdin(9)
    icc.run()
    self.assertEqual(icc.read_stdout(), 0)

  def test_equals_immediate1(self):
    icc = IntCodeComputer()
    icc.load("3,3,1108,-1,8,3,4,3,99")
    icc.put_stdin(8)
    icc.run()
    self.assertEqual(icc.read_stdout(), 1)

  def test_equals_immediate2(self):
    icc = IntCodeComputer()
    icc.load("3,3,1108,-1,8,3,4,3,99")
    icc.put_stdin(12)
    icc.run()
    self.assertEqual(icc.read_stdout(), 0)

  def test_lessthan1(self):
    icc = IntCodeComputer()
    icc.load("3,9,7,9,10,9,4,9,99,-1,8")
    icc.put_stdin(5)
    icc.run()
    self.assertEqual(icc.read_stdout(), 1)

  def test_lessthan2(self):
    icc = IntCodeComputer()
    icc.load("3,9,7,9,10,9,4,9,99,-1,8")
    icc.put_stdin(12)
    icc.run()
    self.assertEqual(icc.read_stdout(), 0)

  def test_lessthan_immediate1(self):
    icc = IntCodeComputer()
    icc.load("3,3,1107,-1,8,3,4,3,99")
    icc.put_stdin(5)
    icc.run()
    self.assertEqual(icc.read_stdout(), 1)

  def test_lessthan_immediate2(self):
    icc = IntCodeComputer()
    icc.load("3,3,1107,-1,8,3,4,3,99")
    icc.put_stdin(12)
    icc.run()
    self.assertEqual(icc.read_stdout(), 0)

  def test_jump_zero(self):
    icc = IntCodeComputer()
    icc.load("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
    icc.put_stdin(0)
    icc.run()
    self.assertEqual(icc.read_stdout(), 0)

  def test_jump_non_zero(self):
    icc = IntCodeComputer()
    icc.load("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
    icc.put_stdin(36)
    icc.run()
    self.assertEqual(icc.read_stdout(), 1)

  def test_jump_zero_immediate(self):
    icc = IntCodeComputer()
    icc.load("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
    icc.put_stdin(0)
    icc.run()
    self.assertEqual(icc.read_stdout(), 0)

  def test_jump_non_zero_immediate(self):
    icc = IntCodeComputer()
    icc.load("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
    icc.put_stdin(36)
    icc.run()
    self.assertEqual(icc.read_stdout(), 1)

  def test_longer_example_day5_1(self):
    icc = IntCodeComputer()
    icc.load("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
    icc.put_stdin(8)
    icc.run()
    self.assertEqual(icc.read_stdout(), 1000)

  def test_longer_example_day5_2(self):
    icc = IntCodeComputer()
    icc.load("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
    icc.put_stdin(7)
    icc.run()
    self.assertEqual(icc.read_stdout(), 999)

  def test_longer_example_day5_3(self):
    icc = IntCodeComputer()
    icc.load("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
    icc.put_stdin(9)
    icc.run()
    self.assertEqual(icc.read_stdout(), 1001)

  def test_example_day9_1(self):
    """ takes no input and produces a copy of itself as output """
    icc = IntCodeComputer()
    icc.load("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
    icc.run()
    self.assertEqual(icc.dump(), [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99])

  def test_example_day9_2(self):
    """ should output a 16-digit number """
    icc = IntCodeComputer()
    icc.load("1102,34915192,34915192,7,4,7,99,0")
    icc.run()
    self.assertEqual(len(str(icc.read_stdout())), 16)

  def test_example_day9_3(self):
    """ should output a 16-digit number """
    icc = IntCodeComputer()
    icc.load("104,1125899906842624,99")
    icc.run()
    self.assertEqual(icc.read_stdout(), 1125899906842624)

if __name__ == '__main__':
    unittest.main(exit=False)

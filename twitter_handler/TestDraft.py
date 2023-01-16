# import unittest
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
#
#
# if __name__ == '__main__':
#     unittest.main()

file = open("res/GreatestQuotes.txt", "r")
cont = file.read()
print(cont)
file.close()

import unittest
from test_cases import TestStringMethods


class RegressionTesting(unittest.TestCase):
    def test_regression(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
        result = unittest.TestResult()
        suite.run(result)

        if result.failures or result.errors:
            print("Regression detected!")
        else:
            print("No regression detected.")


if __name__ == "__main__":
    unittest.main()

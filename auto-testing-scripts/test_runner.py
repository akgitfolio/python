import unittest
from HTMLTestRunner import HTMLTestRunner


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(".", pattern="test_cases.py")

    runner = HTMLTestRunner(output="test_reports")
    runner.run(suite)


if __name__ == "__main__":
    run_tests()

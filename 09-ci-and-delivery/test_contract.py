import unittest
from contract import validate

class TestContract(unittest.TestCase):
    def test_accepts_documented_scores(self):
        self.assertEqual(validate({'odd': 0.9, 'at_least_five': 0.2})['odd'], 0.9)

    def test_rejects_mismatched_or_invalid_scores(self):
        for value in ({'odd': 0.9}, {'odd': 0.9, 'at_least_five': float('nan')},
                      {'odd': True, 'at_least_five': 0.2}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate(value)

if __name__ == '__main__':
    unittest.main()

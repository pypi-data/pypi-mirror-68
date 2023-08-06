import unittest
from strix import value_validation as valid


class TestFromGCA(unittest.TestCase):

    def test_decimal_degree_validate(self):
        # Valid Coordinate
        self.assertEqual(valid.decimal_degree_validate("0"), 0)
        self.assertEqual(valid.decimal_degree_validate("-0"), 0)
        self.assertEqual(valid.decimal_degree_validate("-0.0"), 0)
        self.assertEqual(valid.decimal_degree_validate(0), 0)
        self.assertEqual(valid.decimal_degree_validate(-0), 0)
        self.assertEqual(valid.decimal_degree_validate(-0.0), 0)

        self.assertEqual(valid.decimal_degree_validate("71"), 71)
        self.assertEqual(valid.decimal_degree_validate("+71"), 71)
        self.assertEqual(valid.decimal_degree_validate("-71"), -71)
        self.assertEqual(valid.decimal_degree_validate(71), 71)
        self.assertEqual(valid.decimal_degree_validate(+71), 71)
        self.assertEqual(valid.decimal_degree_validate(-71), -71)

        self.assertEqual(valid.decimal_degree_validate("71.0"), 71.0)
        self.assertEqual(valid.decimal_degree_validate("+71.0"), 71.0)
        self.assertEqual(valid.decimal_degree_validate("-71.0"), -71.0)
        self.assertEqual(valid.decimal_degree_validate(71.0), 71.0)
        self.assertEqual(valid.decimal_degree_validate(+71.0), 71.0)
        self.assertEqual(valid.decimal_degree_validate(-71.0), -71.0)

        self.assertEqual(valid.decimal_degree_validate("71.123456789"), 71.123456789)
        self.assertEqual(valid.decimal_degree_validate("-71.123456789"), -71.123456789)
        self.assertEqual(valid.decimal_degree_validate(71.123456789), 71.123456789)
        self.assertEqual(valid.decimal_degree_validate(-71.123456789), -71.123456789)

        self.assertEqual(valid.decimal_degree_validate("401.00"), 401.00)
        self.assertEqual(valid.decimal_degree_validate(401.00), 401.00)

        # valid as number, but invalid as string
        self.assertEqual(valid.decimal_degree_validate(.01), .01)
        self.assertEqual(valid.decimal_degree_validate(-.01), -.01)

        # Invalid Coordinate
        self.assertRaises(ValueError, valid.decimal_degree_validate, ".01")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "-.01")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "a")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "7a")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "-71.1234 56789")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "-71.k56789")
        self.assertRaises(ValueError, valid.decimal_degree_validate, ".01")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "-.01")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "a")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "7a")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "-71.1234 56789")
        self.assertRaises(ValueError, valid.decimal_degree_validate, "-71.k56789")


if __name__ == '__main__':
    unittest.main()

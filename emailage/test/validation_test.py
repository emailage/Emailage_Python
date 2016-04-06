import unittest

from emailage import validation


class ValidationTest(unittest.TestCase):
    
    def setUp(self):
        self.correct_email = 'test+emailage@example.com'
        self.incorrect_email = 'test+example.com'
        self.correct_ip = '1.234.56.7'
        self.incorrect_ip = '1.23.456.7890'

    def test_validates_email(self):
        validation.assert_email(self.correct_email)
        self.assertRaises(ValueError, validation.assert_email, self.incorrect_email)
        self.assertRaises(ValueError, validation.assert_email, self.correct_ip)
        self.assertRaises(ValueError, validation.assert_email, self.incorrect_ip)

    def test_validates_ip(self):
        validation.assert_ip(self.correct_ip)
        self.assertRaises(ValueError, validation.assert_ip, self.incorrect_ip)
        self.assertRaises(ValueError, validation.assert_ip, self.correct_email)
        self.assertRaises(ValueError, validation.assert_ip, self.incorrect_email)

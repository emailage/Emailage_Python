import unittest

from emailage import validation


class ValidationTest(unittest.TestCase):
    
    def setUp(self):
        self.correct_email = 'test+emailage@example.com'
        self.incorrect_email = 'test+example.com'
        self.correct_ip = '1.234.56.7'
        self.incorrect_ip = '1.23.456.7890'

        self.ipv6_samples_valid = [
            '2001:db8:a0b:12f0::1',
            'FE80:0000:0000:0000:0202:B3FF:FE1E:8329',
            '2607:f0d0:1002:0051:0000:0000:0000:0004',
            'FE80::0202:B3FF:FE1E:8329',
            '2001:0:9d38:90d7:301f:1c10:3f57:fe64'
        ]

        self.ipv6_samples_invalid = [
            '1200::AB00:1234::2552:7777:1313',
            '20::afd34:32::42',
            '1200:0000:AB00:1234:O000:2552:7777:1313'
        ]

        self.ipv4_samples_valid = [
            '255.255.255.255',
            '174.70.13.43',
            '208.67.222.222',
            '192.168.1.155',
            '10.232.222.212',
            '10.123.56.25',
            '155.1.0.1',
            '10.123.0.25',
            '255.0.1.1',
            '255.1.0.255',
            '255.255.255.0',
        ]

        self.ipv4_samples_invalid = [
            '1.1.1:2823',
            '10001.fff45.222.1000:01',
            '192.168.1.1:443',
            '0.0.0.1',
            '0.0.0.0',
            '256.0.0.0',
            '256.0.0.1',
            '155.0.0.',
            '256.0.0.',
            '256.255.255.255',
            '25.255.255.256',
            '255.256.1.1',
            '255.255...',
            '255.255.',
            '255.255.255',
            '255.255.255.',

            '255.1.255.260'
        ]

    def test_validates_valid_ipv4(self):
        failed_ips = []
        ip_data_source = self.ipv4_samples_valid
        for ipv4 in ip_data_source:
            try:
                validation.assert_ip(ipv4)
            except ValueError as exc:
                failed_ips.append(ipv4)

        self.assertListEqual([], failed_ips)

    def test_validates_invalid_ipv4(self):
        failed_ips = []
        ip_data_source = self.ipv4_samples_invalid
        for ipv4 in ip_data_source:
            try:
                self.assertRaises(ValueError, validation.assert_ip, ipv4)
            except Exception as exc:
                failed_ips.append(ipv4)

        self.assertListEqual([], failed_ips)

    def test_validates_email(self):
        validation.assert_email(self.correct_email)
        self.assertRaises(ValueError, validation.assert_email, self.incorrect_email)
        self.assertRaises(ValueError, validation.assert_email, self.correct_ip)
        self.assertRaises(ValueError, validation.assert_email, self.incorrect_ip)

    def test_validates_ip(self):
        for entry in self.ipv6_samples_valid:
            validation.assert_ip(entry)

        self.assertRaises(ValueError, validation.assert_ip, self.correct_email)
        self.assertRaises(ValueError, validation.assert_ip, self.incorrect_email)


if __name__ == '__main__':
    unittest.main()

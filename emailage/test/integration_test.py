import os
import urllib
import unittest

from emailage.client import ApiDomains
from emailage.client import EmailageClient

use_urlparse = hasattr(urllib, 'quote')

if use_urlparse:
    import urlparse
    _parse_qs = urlparse.parse_qs
else:
    _parse_qs = urllib.parse.parse_qs


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        self.api_secret = os.getenv('ENV_SECRET') or 'TEST_SECRET'
        self.api_token = os.getenv('ENV_TOKEN') or 'TEST_TOKEN'

        if self.api_secret == 'TEST_SECRET' and self.api_token == 'TEST_TOKEN':
            raise AssertionError("Ensure you have set valid login credentials in your environment")

        self.api_domain = os.getenv('ENV_DOMAIN') or ApiDomains.sandbox
        self.api_user_email = os.getenv('ENV_USER_EMAIL') or 'user.name@emailage.com'

        self.client_instance = EmailageClient(self.api_secret, self.api_token)
        self.client_instance.set_api_domain(self.api_domain)

        self.test_query_email = 'tumbled.email+inbox@gmail.com'
        self.test_query_ip = '13.25.10.245'

        self.no_spaces_params = {
            'first_name': 'Johann',
            'last_name': 'Vandergrift',
            'phone': '+14805559163'
        }

        self.spaces_params_first_name = {
            'first_name': 'Johann Paulus',
            'last_name': 'Vandergrift',
            'phone': '+14805559163'
        }

        self.spaces_params_last_name = {
            'first_name': 'Johann',
            'last_name': 'van der Grift',
            'phone': '+14805559163'
        }

        self.responseStatusSuccess = {
            'status': 'success',
            'errorCode': '0',
            'description': ''
        }

    def test_trivial_client_query(self):

        test_query_email = 'johann.vandergrift@emailage.com'

        params = {
            'user_email': self.api_user_email,
        }

        response = self.client_instance.query(test_query_email, **params)

        self.assertIsNotNone(response)
        self.assertDictEqual(response['responseStatus'], self.responseStatusSuccess)

        self.assertEqual(response['query']['email'], test_query_email)

    def test_trivial_email_ip_client_query(self):

        test_query_tuple = (self.test_query_email, self.test_query_ip)

        params = {
            'user_email': self.api_user_email
        }

        response = self.client_instance.query(test_query_tuple, **params)

        self.assertIsNotNone(response)
        self.assertDictEqual(response['responseStatus'], self.responseStatusSuccess)
        self.assertEqual(response['query']['email'], self.test_query_email + '+' + self.test_query_ip)

    def test_email_optional_params_no_spaces_client_query(self):

        self.no_spaces_params['user_email'] = self.api_user_email

        response = self.client_instance.query(self.test_query_email, **self.no_spaces_params)

        self.assertIsNotNone(response)
        self.assertDictEqual(response['responseStatus'], self.responseStatusSuccess)
        self.assertEqual(response['query']['email'], self.test_query_email)

    def test_email_ip_optional_params_no_spaces_client_query(self):

        test_query_tuple = (self.test_query_email, self.test_query_ip)

        self.no_spaces_params['user_email'] = self.api_user_email

        response = self.client_instance.query(test_query_tuple, **self.no_spaces_params)

        self.assertIsNotNone(response)
        self.assertDictEqual(response['responseStatus'], self.responseStatusSuccess)
        self.assertEqual(response['query']['email'], self.test_query_email + '+' + self.test_query_ip)

    def test_email_optional_params_first_name_space_client_query(self):

        self.spaces_params_first_name['user_email'] = self.api_user_email

        response = self.client_instance.query(self.test_query_email, **self.spaces_params_first_name)

        self.assertIsNotNone(response)
        self.assertDictEqual(response['responseStatus'], self.responseStatusSuccess)
        self.assertEqual(response['query']['email'], self.test_query_email)

    def test_email_ip_optional_params_first_name_space_client_query(self):

        test_query_tuple = (self.test_query_email, self.test_query_ip)

        self.spaces_params_first_name['user_email'] = self.api_user_email

        response = self.client_instance.query(test_query_tuple, **self.spaces_params_first_name)

        self.assertIsNotNone(response)
        self.assertDictEqual(response['responseStatus'], self.responseStatusSuccess)
        self.assertEqual(response['query']['email'], self.test_query_email + '+' + self.test_query_ip)

    def test_email_optional_params_last_name_space_client_query(self):

        self.spaces_params_last_name['user_email'] = self.api_user_email

        response = self.client_instance.query(self.test_query_email, **self.spaces_params_last_name)

        self.assertIsNotNone(response)
        self.assertDictEqual(response['responseStatus'], self.responseStatusSuccess)
        self.assertEqual(response['query']['email'], self.test_query_email)

    def test_email_ip_optional_params_last_name_space_client_query(self):

        test_query_tuple = (self.test_query_email, self.test_query_ip)

        self.spaces_params_last_name['user_email'] = self.api_user_email

        response = self.client_instance.query(test_query_tuple, **self.spaces_params_last_name)

        self.assertIsNotNone(response)
        self.assertDictEqual(response['responseStatus'], self.responseStatusSuccess)
        self.assertEqual(response['query']['email'], self.test_query_email + '+' + self.test_query_ip)


if __name__ == '__main__':
    unittest.main()

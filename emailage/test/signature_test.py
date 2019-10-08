"""Samples given according to http://oauth.net/core/1.0/#sig_base_example"""
from __future__ import print_function
import unittest

from emailage import signature


class SignatureTest(unittest.TestCase):
    
    def setUp(self):
        self.method = 'GET'
        self.url = 'http://photos.example.net/photos'
        self.params = dict(
            oauth_consumer_key='dpf43f3p2l4k3l03',
            oauth_token='nnch734d00sl2jdk',
            oauth_signature_method='HMAC-SHA1',
            oauth_timestamp=1191242096,
            oauth_nonce='kllo9940pd9333jh',
            oauth_version=1.0,
            file='vacation.jpg',
            size='original'
        )
        self.hmac_key = 'kd94hf93k423kf44&pfkkdhi9sl3r4s00'

        self.test_query_email = 'tumbled.email+inbox@gmail.com'
        self.test_query_ip = '13.25.10.245'

        self.no_spaces_params = {
            'firstname': 'Johann',
            'lastname': 'Vandergrift',
            'phone': '+14805559163'
        }

        self.spaces_params_first_name = {
            'firstname': 'Johann Paulus',
            'lastname': 'Vandergrift',
            'phone': '+14805559163'
        }

        self.spaces_params_last_name = {
            'firstname': 'Johann',
            'lastname': 'van der Grift',
            'phone': '+14805559163'
        }

        self.responseStatusSuccess = {
            'status': 'success',
            'errorCode': '0',
            'description': ''
        }

    def _add_test_oauth_params_to_request_dict(self, request_dict):
        request_dict['oauth_consumer_key'] = 'dpf43f3p2l4k3l03'
        request_dict['oauth_token'] = 'nnch734d00sl2jdk'
        request_dict['oauth_signature_method'] = 'HMAC-SHA1'
        request_dict['oauth_timestamp'] = 1191242096
        request_dict['oauth_nonce'] = 'kllo9940pd9333jh'
        request_dict['oauth_version'] = 1.0
        return request_dict

    def test_normalizes_query_parameters(self):
        query = signature.normalize_query_parameters(self.params)
        self.assertEqual(query, 'file=vacation.jpg&oauth_consumer_key=dpf43f3p2l4k3l03&oauth_nonce=kllo9940pd9333jh&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1191242096&oauth_token=nnch734d00sl2jdk&oauth_version=1.0&size=original')

    def test_normalizes_query_spaces_in_first_name(self):
        query_dict = self._add_test_oauth_params_to_request_dict(self.spaces_params_first_name)

        normalized_qs = signature.normalize_query_parameters(query_dict)

        self.assertTrue(normalized_qs.index('%20'))

    def test_generates_base_string_spaces_in_first_name(self):
        query_dict = self._add_test_oauth_params_to_request_dict(self.spaces_params_first_name)
        query_dict['query'] = self.test_query_email

        normalized_qs = signature.normalize_query_parameters(query_dict)
        base_string = signature.concatenate_request_elements(self.method, self.url, normalized_qs)

        self.assertTrue(base_string.index('%2520'))

    def test_generates_base_string(self):
        query = signature.normalize_query_parameters(self.params)
        base_string = signature.concatenate_request_elements(self.method, self.url, query)
        self.assertEqual(base_string, 'GET&http%3A%2F%2Fphotos.example.net%2Fphotos&file%3Dvacation.jpg%26oauth_consumer_key%3Ddpf43f3p2l4k3l03%26oauth_nonce%3Dkllo9940pd9333jh%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1191242096%26oauth_token%3Dnnch734d00sl2jdk%26oauth_version%3D1.0%26size%3Doriginal')

    def test_calculates_signature_value(self):
        result = signature.create(self.method, self.url, self.params, self.hmac_key)
        self.assertEqual(result, 'tR3+Ty81lMeYAr/Fid0kMTYa/WM=')


if __name__ == '__main__':
    unittest.main()

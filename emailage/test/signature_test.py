"""Samples given according to http://oauth.net/core/1.0/#sig_base_example"""

import unittest

from emailage import signature


class SignatureTest(unittest.TestCase):
    
    def setUp(self):
        self.method = 'GET'
        self.url = 'http://photos.example.net/photos'
        self.params = dict(
            oauth_consumer_key= 'dpf43f3p2l4k3l03',
            oauth_token= 'nnch734d00sl2jdk',
            oauth_signature_method= 'HMAC-SHA1',
            oauth_timestamp= 1191242096,
            oauth_nonce= 'kllo9940pd9333jh',
            oauth_version= 1.0,
            file= 'vacation.jpg',
            size= 'original'
        )
        self.hmac_key = 'kd94hf93k423kf44&pfkkdhi9sl3r4s00'

    def test_normalizes_query_parameters(self):
        query = signature.normalize_query_parameters(self.params)
        self.assertEqual(query, 'file=vacation.jpg&oauth_consumer_key=dpf43f3p2l4k3l03&oauth_nonce=kllo9940pd9333jh&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1191242096&oauth_token=nnch734d00sl2jdk&oauth_version=1.0&size=original')

    def test_generates_base_string(self):
        query = signature.normalize_query_parameters(self.params)
        base_string = signature.concatenate_request_elements(self.method, self.url, query)
        self.assertEqual(base_string, 'GET&http%3A%2F%2Fphotos.example.net%2Fphotos&file%3Dvacation.jpg%26oauth_consumer_key%3Ddpf43f3p2l4k3l03%26oauth_nonce%3Dkllo9940pd9333jh%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1191242096%26oauth_token%3Dnnch734d00sl2jdk%26oauth_version%3D1.0%26size%3Doriginal')

    def test_calculates_signature_value(self):
        result = signature.create(self.method, self.url, self.params, self.hmac_key)
        self.assertEqual(result, 'tR3+Ty81lMeYAr/Fid0kMTYa/WM=')

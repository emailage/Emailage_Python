import unittest
import urllib
from mock import Mock
from emailage import protocols
from emailage.client import EmailageClient


use_urlparse = hasattr(urllib, 'quote')

if use_urlparse:
    import urlparse
    _parse_qs = urlparse.parse_qs
else:
    _parse_qs = urllib.parse.parse_qs


class ClientTest(unittest.TestCase):

    _tls_version = None

    def setUp(self):
        response = Mock()
        response.content = b'\xEF\xBB\xBF{"success":[true]}'
        response.text = str(response.content)
        
        self.email = 'test+emailage@example.com'
        self.ip = '1.234.56.7'

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

        if self._tls_version is not None:
            self.subj = EmailageClient('secret', 'token', sandbox=True, tls_version=self._tls_version)
        else:
            self.subj = EmailageClient('secret', 'token', sandbox=True)

        self.g = self.subj.session.get = Mock(return_value=response)

    def test_is_initialized_with_properties(self):
        self.assertTrue(self.subj.sandbox)

    def test_generates_appropriate_key(self):
        self.assertEqual(self.subj.hmac_key, 'token&')


class ClientRequestTest(ClientTest):
    
    def _request(self):
        return self.subj.request('/endpoint', query='something')
    
    def test_request__call(self):
        """Targets requests to the correct endpoint with correct request params"""
        self._request()
        call_args = self.g.call_args_list[0]
        url = call_args[0][0]
        params = _parse_qs(call_args[1]['params'])

        self.assertEqual(url, 'https://sandbox.emailage.com/emailagevalidator/endpoint/')
        self.assertEqual(params['query'][0], 'something')
        self.assertEqual(params['oauth_consumer_key'][0], 'secret')
    
    def test_request__returns(self):
        """Parses response body as JSON"""
        self.assertEqual(self._request(), {'success': [True]})
        
        
class ClientQueryTest(ClientTest):
    
    def test_query(self):
        """Concatenates arguments and passes extra params to request"""
        self.r = self.subj.request = Mock()
        self.subj.query((self.email, self.ip), urid=1234567890)
        
        self.r.assert_called_once_with('', urid=1234567890, query='test+emailage@example.com+1.234.56.7')
        
        
class ClientFlagTest(ClientTest):
    
    def setUp(self):
        super(ClientFlagTest, self).setUp()
        self.r = self.subj.request = Mock()

    def test_flag_as_fraud__call(self):
        """Flags a supplied address as fraud with an appropriate fraud code"""
        self.subj.flag_as_fraud(self.email, 3)
        
        self.r.assert_called_once_with('/flag', flag='fraud', query='test+emailage@example.com', fraudcodeID=3)

    def test_flag_as_fraud__call2(self):
        """Flags a supplied address as fraud with fraud code = 9 if the code is an integer but out of range"""
        self.subj.flag_as_fraud(self.email, 42)
        
        self.r.assert_called_once_with('/flag', flag='fraud', query='test+emailage@example.com', fraudcodeID=9)
            
    def test_flag_as_fraud__exceptions(self):
        """Raises an error when none, unknown or string fraud code is supplied"""
        self.assertRaises(TypeError, self.subj.flag_as_fraud, self.email)
        self.assertRaises(ValueError, self.subj.flag_as_fraud, self.email, 'Blah blah')
        self.assertRaises(ValueError, self.subj.flag_as_fraud, self.email, 'First Party Fraud')
    
    def test_flag_as_good(self):
        """Flags a supplied address as good"""
        self.subj.flag_as_good(self.email)
        
        self.r.assert_called_once_with('/flag', flag='good', query=self.email)

    def test_remove_flag(self):
        """Unflags a supplied address"""
        self.subj.remove_flag(self.email)
        
        self.r.assert_called_once_with('/flag', flag='neutral', query=self.email)


class ClientTls11Test(ClientQueryTest, ClientRequestTest):

    @classmethod
    def setUpClass(cls):
        cls._tls_version = protocols.TLSv1_1


class ClientTls12Test(ClientQueryTest, ClientRequestTest):

    @classmethod
    def setUpClass(cls):
        cls._tls_version = protocols.TLSv1_2


class ClientTls11FlagTest(ClientFlagTest):

    @classmethod
    def setUpClass(cls):
        cls._tls_version = protocols.TLSv1_1


class ClientTls12FlagTest(ClientFlagTest):

    @classmethod
    def setUpClass(cls):
        cls._tls_version = protocols.TLSv1_2


if __name__ == '__main__':
    unittest.main()


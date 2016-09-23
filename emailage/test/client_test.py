import unittest
from mock import Mock
import requests

from emailage.client import EmailageClient


class ClientTest(unittest.TestCase):
    
    def setUp(self):
        response = Mock()
        response.text = '\xEF\xBB\xBF{"success":[true]}'
        
        self.email = 'test+emailage@example.com'
        self.ip = '1.234.56.7'
        
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
        params = call_args[1]['params']
        
        self.assertEqual(url, 'https://sandbox.emailage.com/emailagevalidator/endpoint/')
        self.assertEqual(params['query'], 'something')
        self.assertEqual(params['oauth_consumer_key'], 'secret')
    
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

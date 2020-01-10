import unittest
import urllib
import requests
from mock import Mock
from emailage import protocols
from emailage.client import EmailageClient, HttpMethods


use_urlparse = hasattr(urllib, 'quote')

if use_urlparse:
    import urlparse
    _parse_qs = urlparse.parse_qs
else:
    _parse_qs = urllib.parse.parse_qs


class RequestsSessionMockup:
    BYTE_ORDER_MARK = [0xEF, 0xBB, 0xBF]

    def __init__(self):
        self._mock_obj = Mock(spec=requests.Session)

    def set_response_for_http_verb(self, http_method, response_content_json):
        func_mock = Mock(return_value=self.get_response_mock(response_content_json))

        if http_method == HttpMethods.GET:
            self._mock_obj.get = func_mock
        elif http_method == HttpMethods.POST:
            self._mock_obj.post = func_mock

    @property
    def mock_object(self):
        return self._mock_obj

    def post(self, *args, **kwargs):
        return self._mock_obj.post(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._mock_obj.get(*args, **kwargs)

    def get_response_mock(self, response_json_content):
        response_mock = Mock(spec=requests.Response)
        content_bytes = list(self.BYTE_ORDER_MARK)

        for string_byte in bytearray(response_json_content, encoding='utf_8'):
            content_bytes.append(string_byte)

        response_mock.content = bytes(content_bytes)
        response_mock.text = str(response_mock.content)
        return response_mock


class ClientTest(unittest.TestCase):

    _tls_version = None
    _http_method = None
    _timeout = None
    mocked_session = None

    def setUp(self):

        self.email = 'test+emailage@example.com'
        self.ip = '1.234.56.7'

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

        if self._tls_version is not None:
            self.subj = EmailageClient('secret',
                                       'token',
                                       sandbox=True,
                                       tls_version=self._tls_version,
                                       timeout=self._timeout)
        else:
            self.subj = EmailageClient('secret', 'token', sandbox=True, timeout=self._timeout)

        if self._http_method is not None:
            self.subj.set_http_method(self._http_method)

        session_mockup = RequestsSessionMockup()
        session_mockup.set_response_for_http_verb(self.subj.http_method, '{"success":[true]}')
        self.mocked_session = session_mockup.mock_object

        self.subj.session = self.mocked_session

    def test_is_initialized_with_properties(self):
        self.assertTrue(self.subj.sandbox)

    def test_generates_appropriate_key(self):
        self.assertEqual(self.subj.hmac_key, 'token&')


class ClientRequestTest(ClientTest):

    def setUp(self):
        super(ClientRequestTest, self).setUp()

    def _request(self):
        return self.subj.request('/endpoint', query='something')

    def test_request__returns(self):
        """Parses response body as JSON"""
        self.assertEqual(self._request(), {'success': [True]})


class ClientGetRequestTest(ClientRequestTest):

    def setUp(self):
        self._http_method = HttpMethods.GET
        super(ClientRequestTest, self).setUp()

    def test_request__call(self):
        """Targets requests to the correct endpoint with correct request params"""
        self._request()
        call_args = self.mocked_session.get.call_args_list[0]
        url = call_args[0][0]
        params = _parse_qs(call_args[1]['params'])

        self.assertEqual(url, 'https://sandbox.emailage.com/emailagevalidator/endpoint/')
        self.assertEqual(params['query'][0], 'something')
        self.assertEqual(params['oauth_consumer_key'][0], 'secret')


class ClientPostRequestTest(ClientRequestTest):

    def setUp(self):
        self._http_method = HttpMethods.POST
        super(ClientPostRequestTest, self).setUp()

    def test_uses_post_http_verb(self):
        """ Ensure that the client uses the verb specified (POST)"""
        self._request()

        called_with_args = self.mocked_session.post.call_args_list

        for entry in called_with_args:
            print(repr(entry))

        self.assertIsNotNone(called_with_args)
        self.assertEqual(self.subj.http_method, self._http_method)


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

    def setUp(self):
        super(ClientRequestTest, self).setUp()

    @classmethod
    def setUpClass(cls):
        cls._tls_version = protocols.TLSv1_1


class ClientTls12Test(ClientQueryTest, ClientRequestTest):

    def setUp(self):
        super(ClientRequestTest, self).setUp()

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


class ClientHttpPostFlagTest(ClientFlagTest):

    @classmethod
    def setUpClass(cls):
        cls._http_method = HttpMethods.POST


class ClientHttpGetFlagTest(ClientFlagTest):

    @classmethod
    def setUpClass(cls):
        cls._http_method = HttpMethods.GET


if __name__ == '__main__':
    unittest.main()

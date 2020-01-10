import json
import ssl
import sys
import urllib

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from emailage import signature, validation
from emailage.signature import safety_quote


use_urllib_quote = hasattr(urllib, 'quote')


if use_urllib_quote:
    def _url_encode_dict(qs_dict):
        return '&'.join(map(lambda pair: '='.join([urllib.quote(str(pair[0]), ''), urllib.quote(str(pair[1]), '')]),
                            sorted(qs_dict.items())))
elif sys.version_info >= (3, 5):
    # Python >= 3.5
    def _url_encode_dict(qs_dict):
        return urllib.parse.urlencode(qs_dict, quote_via=urllib.parse.quote)
else:
    # Python 3.x - 3.4
    def _url_encode_dict(qs_dict):
        return '&'.join(map(lambda pair: '='.join([urllib.parse.quote(str(pair[0]), ''),
                                                   urllib.parse.quote(str(pair[1]), '')]),
                            sorted(qs_dict.items())))


class TlsVersions:
    """An enumeration of the TLS versions supported by the Emailage API"""
    TLSv1_1 = ssl.PROTOCOL_TLSv1_1
    TLSv1_2 = ssl.PROTOCOL_TLSv1_2


class ApiDomains:
    """API URLs for the specified domains """
    sandbox = 'https://sandbox.emailage.com'
    production = 'https://api.emailage.com'


class HttpMethods:
    """HttpMethod constants to pass to the client"""
    GET = 'GET'
    POST = 'POST'


class EmailageClient:
    """ Primary proxy to the Emailage API for end-users of the package"""
    FRAUD_CODES = {
        1: 'Card Not Present Fraud',
        2: 'Customer Dispute (Chargeback)',
        3: 'First Party Fraud',
        4: 'First Payment Default',
        5: 'Identify Theft (Fraud Application)',
        6: 'Identify Theft (Account Take Over)',
        7: 'Suspected Fraud (Not Confirmed)',
        8: 'Synthetic ID',
        9: 'Other'
    }

    class Adapter(HTTPAdapter):
        def __init__(self, tls_version=TlsVersions.TLSv1_2):
            self._tls_version = tls_version
            self.poolmanager = None
            super(EmailageClient.Adapter, self).__init__()

        def init_poolmanager(self, connections, maxsize, block=False):
            self.poolmanager = PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=self._tls_version)

    def __init__(
        self,
        secret,
        token,
        sandbox=False,
        tls_version=TlsVersions.TLSv1_2,
        timeout=None,
        http_method='GET'
    ):
        """ Creates an instance of the EmailageClient using the specified credentials and environment

            :param secret: Consumer secret, e.g. SID or API key.
            :param token: Consumer token.
            :param sandbox:
                (Optional) Whether to use a sandbox instead of a production server. Uses production by default
            :param tls_version: (Optional) Uses TLS version 1.2 by default (TlsVersions.TLSv1_2 | TlsVersions.TLSv1_1)
            :param timeout: (Optional) The timeout to be used for sent requests
            :param http_method: (Optional) The HTTP method (GET or POST) to be used for sending requests

            :type secret: str
            :type token: str
            :type sandbox: bool
            :type tls_version: see :class:`TlsVersions`
            :type timeout: float
            :type http_method: see :class:`HttpMethods`

            :Example:

            >>> from emailage.client import EmailageClient
            >>> from emailage import protocols
            >>> client = EmailageClient('consumer_secret', 'consumer_token', sandbox=True, tls_version=protocols.TLSv1_1)
            >>> fraud_report = client.query(('useremail@example.co.uk', '192.168.1.1'), urid='some_unique_identifier')
            
            :Example:

            >>> from emailage.client import EmailageClient
            >>> from emailage import protocols
            >>> client = EmailageClient('consumer_secret', 
            ...                         'consumer_token', sandbox=True, timeout=300)
            >>> fraud_report = client.query(('useremail@example.co.uk', '192.168.1.1'), urid='some_unique_identifier')

        """
        self.secret, self.token, self.sandbox = secret, token, sandbox
        self.timeout = timeout
        self.hmac_key = token + '&'
        self.session = None
        self.domain = None
        self.set_api_domain((sandbox and ApiDomains.sandbox or ApiDomains.production), tls_version)
        self._http_method = http_method.upper()

    def set_credentials(self, secret, token):
        """ Explicitly set the authentication credentials to be used when generating a request in the current session.
            Useful when you want to change credentials after initial creation of the client.

            :param secret: Consumer secret, e.g. SID or API key
            :param token: Consumer token
            :return: None

        """
        self.secret = secret
        self.token = token
        self.hmac_key = token + '&'

    def set_api_domain(self, domain, tls_version=TlsVersions.TLSv1_2):
        """ Explicitly set the API domain to use for a session of the client, typically used in testing scenarios

            :param domain: API domain to use for the session
            :param tls_version: (Optional) Uses TLS version 1.2 by default (TlsVersions.TLSv1_2 | TlsVersions.TLSv1_1)
            :return: None

            :type domain: str see :class: `ApiDomains`
            :type tls_version: see :class: `TlsVersions`

            :Example:

            >>> from emailage.client import EmailageClient
            >>> from emailage.client import ApiDomains
            >>> client = EmailageClient('consumer_secret', 'consumer_token')
            >>> client.set_api_domain(ApiDomains.sandbox)
            >>> client.domain
            'https://sandbox.emailage.com'

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('consumer_secret', 'consumer_token')
            >>> client.set_api_domain('https://testing.emailage.com')
            >>> client.domain
            'https://testing.emailage.com'
        """
        self.session = Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.domain = domain
        self.session.mount(self.domain, EmailageClient.Adapter(tls_version))

    def set_http_method(self, http_method):
        """ Explicitly set the Http method (GET or POST) through which you will be sending the request. This method
            will be used for any future calls made with this instance of the client until another method is specified

            :param http_method: HttpMethod to use for sending requests
            :return: None

            :type http_method: str see :class: `HttpMethods`

            :Example:

            >>> from emailage.client import EmailageClient, HttpMethods
            >>> client = EmailageClient('consumer_secret', 'consumer_token')
            >>> client.set_http_method(HttpMethods.POST)
            >>> client.http_method
            'POST'
        """
        if not http_method:
            raise TypeError('http_method must be a string with the value GET or SET')

        if not http_method.upper() == HttpMethods.GET and not http_method.upper() == HttpMethods.POST:
            raise ValueError('http_method must be a string with the value GET or SET')

        self._http_method = http_method.upper()

    @property
    def http_method(self):
        return self._http_method

    def request(self, endpoint, **params):
        """ Base method to generate requests for the Emailage validator and flagging APIs

            :param endpoint: API endpoint to send the request ( '' | '/flag' )
            :param params: keyword-argument list of parameters to send with the request
            :return: JSON dict of the response generated by the API

            :type endpoint: str
            :type params: kwargs

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('consumer_secret', 'consumer_token')
            >>> response = client.request('/flag', email='user20180830001@domain20180830001.com', flag='good')
            >>> response['query']['email']
            u'user20180830001%40domain20180830001.com'
        """
        url = self.domain + '/emailagevalidator' + endpoint + '/'
        api_params = dict(
            format='json',
            **params
        )

        request_params = {}
        if self.timeout is not None and 'timeout':
            request_params['timeout'] = self.timeout

        if self.http_method == HttpMethods.GET:
            response = self._perform_get_request(url, api_params, request_params)
        else:
            response = self._perform_post_request(url, api_params, request_params)

        if not response:
            raise ValueError('No response received for request')

        # Explicit encoding is necessary because the API returns a Byte Order Mark at the beginning of the contents
        json_data = response.content.decode(encoding='utf_8_sig')
        return json.loads(json_data)

    def _perform_get_request(self, url, api_params, request_params=None):

        api_params = signature.add_oauth_entries_to_fields_dict(self.secret, api_params)
        api_params['oauth_signature'] = signature.create(HttpMethods.GET, url, api_params, self.hmac_key)

        params_qs = _url_encode_dict(api_params)
        request_params = request_params or {}

        res = self.session.get(url, params=params_qs, **request_params)
        return res

    def _perform_post_request(self, url, api_params, request_params=None):
        signature_fields = dict(format='json')

        signature_fields = signature.add_oauth_entries_to_fields_dict(self.secret, signature_fields)

        signature_fields['oauth_signature'] = signature.create(HttpMethods.POST, url, signature_fields, self.hmac_key)
        url = url + '?' + _url_encode_dict(signature_fields)

        payload = bytes(self._assemble_quoted_pairs(api_params), encoding='utf_8')

        res = self.session.post(url, data=payload, **request_params)
        return res

    @staticmethod
    def _assemble_quoted_pairs(kv_pairs):
        return '&'.join(map(lambda pair: '='.join([safety_quote(pair[0]),
                                                   safety_quote(pair[1])]),
                            sorted(kv_pairs.items())))

    def query(self, query, **params):
        """ Base query method providing support for email, IP address, and optional additional parameters

            :param query: RFC2822-compliant Email, RFC791-compliant IP, or both
            :param params: keyword-argument form for parameters such as urid, first_name, last_name, etc.
            :return: JSON dict of the response generated by the API

            :type query: str | (str, str)
            :type params: kwargs

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('consumer_secret', 'consumer_token')
            >>> response_json = client.query('test@example.com')
            >>> # Email address only
            >>> response_json = client.query('test@example.com')
            >>> # IP Address only
            >>> response_json = client.query('209.85.220.41')
            >>> # For a combination. Please note the order
            >>> response_json = client.query(('test@example.com', '209.85.220.41'))
            >>> # Pass a User Defined Record ID (URID) as an optional parameter
            >>> response_json = client.query('test@example.com', urid='My record ID for test@example.com')
        """
        if type(query) is tuple:
            validation.assert_email(query[0])
            validation.assert_ip(query[1])
            query = '+'.join(query)
        params['query'] = query
        return self.request('', **params)

    def query_email(self, email, **params):
        """Query a risk score information for the provided email address.

            :param email: RFC2822-compliant Email
            :param params: (Optional) keyword-argument form for parameters such as urid, first_name, last_name, etc.

            :return: JSON dict of the response generated by the API

            :type email: str
            :type params: kwargs

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
            >>> response_json = client.query_email('test@example.com')
        """
        validation.assert_email(email)
        return self.query(email, **params)

    def query_ip_address(self, ip, **params):
        """Query a risk score information for the provided IP address.

            :param ip: RFC791-compliant IP
            :param params: (Optional) keyword-argument form for parameters such as urid, first_name, last_name, etc.
            :return: JSON dict of the response generated by the API

            :type ip: str
            :type params: kwargs

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
            >>> response_json = client.query_ip_address('209.85.220.41')
        """
        validation.assert_ip(ip)
        return self.query(ip, **params)

    def query_email_and_ip_address(self, email, ip, **params):
        """Query a risk score information for the provided combination of an Email and IP address

            :param email: RFC2822-compliant Email
            :param ip: RFC791-compliant IP
            :param params: (Optional) keyword-argument form for parameters such as urid, first_name, last_name, etc.
            :return: JSON dict of the response generated by the API

            :type email: str
            :type ip: str
            :type params: kwargs

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
            >>> response_json = client.query_email_and_ip_address('test@example.com', '209.85.220.41')

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
            >>> response_json = client.query_email_and_ip_address('test@example.com', '209.85.220.41',
            ...     urid='My record ID for test@example.com and 209.85.220.41')

        """
        validation.assert_email(email)
        validation.assert_ip(ip)
        return self.query((email, ip), **params)

    def flag(self, flag, query, fraud_code=None):
        """ Base method used to flag an email address as fraud, good, or neutral

            :param flag: type of flag you wish to associate with the identifier ( 'fraud' | 'good' | 'neutral' )
            :param query: Email to be flagged
            :param fraud_code:
                (Optional) Required if flag is 'fraud', one of the IDs in `emailage.client.EmailageClient.FRAUD_CODES`

            :return: JSON dict of the confirmation response generated by the API

            :type flag: str
            :type query: str
            :type fraud_code: int

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
            >>> response_json = client.flag('good', 'test@example.com')
            >>> response_json = client.flag('fraud', 'test@example.com', fraud_code=6)
            >>> response_json = client.flag('neutral', 'test@example.com')

        """
        flags = ['fraud', 'neutral', 'good']
        if flag not in flags:
            raise ValueError(validation.Messages.FLAG_NOT_ALLOWED_FORMAT.format(', '.join(flags), flag))

        validation.assert_email(query)

        params = dict(flag=flag, query=query)

        if flag == 'fraud':
            codes = self.FRAUD_CODES
            if type(fraud_code) is not int:
                raise ValueError(
                    validation.Messages.FRAUD_CODE_RANGE_FORMAT.format(
                        len(codes), ', '.join(codes.values()), fraud_code)
                )
            if fraud_code not in range(1, len(codes) + 1):
                fraud_code = 9
            params['fraudcodeID'] = fraud_code

        return self.request('/flag', **params)

    def flag_as_fraud(self, query, fraud_code):
        """Mark an email address as fraud.

            :param query: Email to be flagged
            :param fraud_code: Reason for the email to be marked as fraud; must be one of the IDs in `emailage.client.EmailageClient.FRAUD_CODES`
            :return: JSON dict of the confirmation response generated by the API

            :type query: str
            :type fraud_code: int

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
            >>> response_json = client.flag_as_fraud('test@example.com', 8)

        """
        return self.flag('fraud', query, fraud_code)

    def flag_as_good(self, query):
        """Mark an email address as good.

            :param query: Email to be flagged
            :return: JSON dict of the confirmation response generated by the API

            :type query: str

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
            >>> response_json = client.flag_as_good('test@example.com')

        """
        return self.flag('good', query)

    def remove_flag(self, query):
        """Unflag an email address that was marked as good or fraud previously.

            :param query: Email to be flagged
            :return: JSON dict of the confirmation response generated by the API

            :type query: str

            :Example:

            >>> from emailage.client import EmailageClient
            >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
            >>> response_json = client.remove_flag('test@example.com')

        """
        return self.flag('neutral', query)

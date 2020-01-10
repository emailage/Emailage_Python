"""OAuth1 module written according to http://oauth.net/core/1.0/#signing_process"""
import base64
import hmac
import requests  # requests must be loaded so that urllib receives the parse module
import time
import urllib

from hashlib import sha1
from six import b
from uuid import uuid4

use_parse_quote = not hasattr(urllib, 'quote')

if use_parse_quote:
    _quote_func = urllib.parse.quote
else:
    _quote_func = urllib.quote


def safety_quote(value):
    return _quote_func(str(value), safe='')


def _quote(obj):
    return _quote_func(str(obj), safe='')


def normalize_query_parameters(params):
    """9.1.1.  Normalize Request Parameters"""
    return '&'.join(map(lambda pair: '='.join([_quote(pair[0]), _quote(pair[1])]), sorted(params.items())))


def concatenate_request_elements(method, url, query):
    """9.1.3.  Concatenate Request Elements"""
    return '&'.join(map(_quote, [str(method).upper(), url, query]))


def hmac_sha1(base_string, hmac_key):
    """9.2.  HMAC-SHA1"""
    hash = hmac.new(b(hmac_key), b(base_string), sha1)
    return hash.digest()


def encode(digest):
    """9.2.1.  Generating Signature"""
    return base64.b64encode(digest).decode('ascii').rstrip('\n')


def add_oauth_entries_to_fields_dict(secret, params, nonce=None, timestamp=None):
    """ Adds dict entries to the user's params dict which are required for OAuth1.0 signature generation

        :param secret: API secret
        :param params: dictionary of values which will be sent in the query
        :param nonce: (Optional) random string used in signature creation, uuid4() is used if not provided
        :param timestamp: (Optional) integer-format timestamp, time.time() is used if not provided
        :return: dict containing params and the OAuth1.0 fields required before executing signature.create

        :type secret: str
        :type params: dict
        :type nonce: str
        :type timestamp: int

        :Example:

        >>> from emailage.signature import add_oauth_entries_to_fields_dict
        >>> query_params = dict(user_email='registered.account.user@yourcompany.com',\
            query='email.you.are.interested.in@gmail.com'\
        )
        >>> query_params = add_oauth_entries_to_fields_dict('YOUR_API_SECRET', query_params)
        >>> query_params['oauth_consumer_key']
        'YOUR_API_SECRET'
        >>> query_params['oauth_signature_method']
        'HMAC-SHA1'
        >>> query_params['oauth_version']
        1.0
    """
    if nonce is None:
        nonce = uuid4()
    if timestamp is None:
        timestamp = int(time.time())

    params['oauth_consumer_key'] = secret
    params['oauth_nonce'] = nonce
    params['oauth_signature_method'] = 'HMAC-SHA1'
    params['oauth_timestamp'] = timestamp
    params['oauth_version'] = 1.0

    return params


def create(method, url, params, hmac_key):
    """ Generates the OAuth1.0 signature used as the value for the query string parameter 'oauth_signature'

        :param method: HTTP method that will be used to send the request ( 'GET' | 'POST' )
        :param url: API domain and endpoint up to the ?
        :param params: user-provided query string parameters and the OAuth1.0 parameters
            :method add_oauth_entries_to_fields_dict:
        :param hmac_key: for Emailage users, this is your consumer token with an '&' (ampersand) appended to the end

        :return: str value used for oauth_signature

        :type method: str
        :type url: str
        :type params: dict
        :type hmac_key: str

        :Example:

        >>> from emailage.signature import add_oauth_entries_to_fields_dict, create
        >>> your_api_key = 'SOME_KEY'
        >>> your_hmac_key = 'SOME_SECRET' + '&'
        >>> api_url = 'https://sandbox.emailage.com/emailagevalidator/'
        >>> query_params = { 'query': 'user.you.are.validating@gmail.com', 'user_email': 'admin@yourcompany.com' }
        >>> query_params = add_oauth_entries_to_fields_dict(your_api_key, query_params)
        >>> query_params['oauth_signature'] = create('GET', api_url, query_params, your_hmac_key)

    """

    query = normalize_query_parameters(params)
    base_string = concatenate_request_elements(method, url, query)
    digest = hmac_sha1(base_string, hmac_key)
    return encode(digest)

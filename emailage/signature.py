"""OAuth1 module written according to http://oauth.net/core/1.0/#signing_process"""

import urllib
from hashlib import sha1
import hmac
import base64
from six import b

if hasattr(urllib, 'quote'):
    def _quote(obj):
        return urllib.quote(str(obj), safe='')
else:
    def _quote(obj):
        return urllib.parse.quote(str(obj), safe='')

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

def create(method, url, params, hmac_key):
    """Using HTTP GET parameters option.

    Args:
        method   (str): HTTP 1.1 Method.
        url      (str): Normalized URL to be requested until ? sign.
        params  (dict): GET or www-urlencoded POST request params.
        hmac_key (str): Key generated out of Consumer secret and token.
        
    Returns:
        str: Value of the oauth_signature query parameter.
    """
    query = normalize_query_parameters(params)
    base_string = concatenate_request_elements(method, url, query)
    digest = hmac_sha1(base_string, hmac_key)
    return encode(digest)

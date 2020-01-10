![alt text](https://www.emailage.com/wp-content/uploads/2018/01/logo-
dark.svg)(https://www.emailage.com)

The Python-language Emailage API client helps companies integrate with our
highly efficient fraud risk and scoring system. By calling our API endpoints
and simply passing us an email and/or IP Address, companies will be provided
with real-time risk scoring assessments based around machine learning and
proprietary algorithms that evolve with new fraud trends.

# Quickstart guide

## Requirements

  * Python 2.7+ or 3.3+

## Installation

The Emailage client can be installed with pip:

    
    
    $ pip install emailage-official
    

or directly from the source code:

    
    
    $ git clone https://github.com/emailage/Emailage_Python.git
    $ cd Emailage_Python
    $ python setup.py install
    

## Typical usage

### Instantiate a client

#### Targeting the production servers

    
    
    from emailage.client import EmailageClient
    client = EmailageClient('My account SID', 'My auth token')
    

#### Targeting the sandbox environment

    
    
    from emailage.client import EmailageClient
    client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    

### Query risk score information for the provided email address, IP address,
or a combination

* * *
    
    
    from emailage.client import EmailageClient
    client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    # For an email address
    client.query('test@example.com')
    # For an IP address
    client.query('127.0.0.1')
    # For a combination. Please note the order
    client.query(('test@example.com', '127.0.0.1'))
    # Pass a User Defined Record ID (URID).
    # Can be used when you want to add an identifier for a query.
    # The identifier will be displayed in the result.
    client.query('test@example.com', urid='My record ID for test@example.com')
    

Explicit methods produce the same request while validating format of the
arguments passed

    
    
    from emailage.client import EmailageClient
    client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    # For an email address
    client.query_email('test@example.com')
    # For an IP address
    client.query_ip_address('127.0.0.1')
    # For a combination. Please note the order
    client.query_email_and_ip_address('test@example.com', '127.0.0.1')
    # Pass a User Defined Record ID
    client.query_email_and_ip_address('test@example.com', '127.0.0.1', urid='My record ID for test@example.com and 127.0.0.1')
    

### Mark an email address as fraud, good, or neutral

* * *

You may report that you have found that an email address is good, is
associated with fraud, or is neither (neutral).

The call to flag an email address as fraud _must_ be accompanied by one of the
fraud reasons enumerated below:

  1. Card Not Present Fraud

  2. Customer Dispute (Chargeback)

  3. First Party Fraud

  4. First Payment Default

  5. Identify Theft (Fraud Application)

  6. Identify Theft (Account Take Over)

  7. Suspected Fraud (Not Confirmed)

  8. Synthetic ID

  9. Other

#### Mark an email address as fraud because of Synthetic ID

    
    
    from emailage.client import EmailageClient
    client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    client.flag('fraud', 'test@example.com', 8)
    client.flag_as_fraud('test@example.com', 8)
    # Mark an email address as good
    client.flag('good', 'test@example.com')
    client.flag_as_good('test@example.com')
    # Unflag an email address that was previously marked as good or fraud
    client.flag('neutral', 'test@example.com')
    client.remove_flag('test@example.com')
    

## Exceptions

This client can throw exceptions on any of the following issues:

  1. When Requests has an issue, like not being able to connect from your server to the Emailage API,

  2. When incorrectly-formatted JSON is received,

  3. When an incorrectly-formatted email or IP address is passed to a flagging or explicit querying method.

# Client API reference

## _module_ `emailage.client`


### _class_ `emailage.client.EmailageClient`( _secret_ , _token_ ,
_sandbox=False_ , _tls_version= <_SSLMethod.PROTOCOL_TLSv1_2: 5>_,
_timeout=None_ , _http_method='GET'_ )

    

Primary proxy to the Emailage API for end-users of the package

Creates an instance of the EmailageClient using the specified credentials and
environment

Parameters

    

  * **secret** ( _str_ )  Consumer secret, e.g. SID or API key.

  * **token** ( _str_ )  Consumer token.

  * **sandbox** ( _bool_ )  (Optional) Whether to use a sandbox instead of a production server. Uses production by default

  * **tls_version** (see `TlsVersions`)  (Optional) Uses TLS version 1.2 by default (TlsVersions.TLSv1_2 | TlsVersions.TLSv1_1)

  * **timeout** ( _float_ )  (Optional) The timeout to be used for sent requests

  * **http_method** (see `HttpMethods`)  (Optional) The HTTP method (GET or POST) to be used for sending requests

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> from emailage import protocols
    >>> client = EmailageClient('consumer_secret', 'consumer_token', sandbox=True, tls_version=protocols.TLSv1_1)
    >>> fraud_report = client.query(('useremail@example.co.uk', '192.168.1.1'), urid='some_unique_identifier')
    

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> from emailage import protocols
    >>> client = EmailageClient('consumer_secret', 
    ...                         'consumer_token', sandbox=True, timeout=300)
    >>> fraud_report = client.query(('useremail@example.co.uk', '192.168.1.1'), urid='some_unique_identifier')
    

`flag`( _flag_ , _query_ , _fraud_code=None_ )

    

Base method used to flag an email address as fraud, good, or neutral

Parameters

    

  * **flag** ( _str_ )  type of flag you wish to associate with the identifier ( fraud | good | neutral )

  * **query** ( _str_ )  Email to be flagged

  * **fraud_code** ( _int_ )  (Optional) Required if flag is fraud, one of the IDs in emailage.client.EmailageClient.FRAUD_CODES

Returns

    

JSON dict of the confirmation response generated by the API

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    >>> response_json = client.flag('good', 'test@example.com')
    >>> response_json = client.flag('fraud', 'test@example.com', fraud_code=6)
    >>> response_json = client.flag('neutral', 'test@example.com')
    

`flag_as_fraud`( _query_ , _fraud_code_ )

    

Mark an email address as fraud.

Parameters

    

  * **query** ( _str_ )  Email to be flagged

  * **fraud_code** ( _int_ )  Reason for the email to be marked as fraud; must be one of the IDs in emailage.client.EmailageClient.FRAUD_CODES

Returns

    

JSON dict of the confirmation response generated by the API

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    >>> response_json = client.flag_as_fraud('test@example.com', 8)
    

`flag_as_good`( _query_ )

    

Mark an email address as good.

Parameters

    

**query** ( _str_ )  Email to be flagged

Returns

    

JSON dict of the confirmation response generated by the API

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    >>> response_json = client.flag_as_good('test@example.com')
    

`query`( _query_ , _**params_ )

    

Base query method providing support for email, IP address, and optional
additional parameters

Parameters

    

  * **query** ( _str |_ _(_ _str_ _,_ _str_ _)_ )  RFC2822-compliant Email, RFC791-compliant IP, or both

  * **params** ( _kwargs_ )  keyword-argument form for parameters such as urid, first_name, last_name, etc.

Returns

    

JSON dict of the response generated by the API

Example

    
    
    
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
    

`query_email`( _email_ , _**params_ )

    

Query a risk score information for the provided email address.

Parameters

    

  * **email** ( _str_ )  RFC2822-compliant Email

  * **params** ( _kwargs_ )  (Optional) keyword-argument form for parameters such as urid, first_name, last_name, etc.

Returns

    

JSON dict of the response generated by the API

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    >>> response_json = client.query_email('test@example.com')
    

`query_email_and_ip_address`( _email_ , _ip_ , _**params_ )

    

Query a risk score information for the provided combination of an Email and IP
address

Parameters

    

  * **email** ( _str_ )  RFC2822-compliant Email

  * **ip** ( _str_ )  RFC791-compliant IP

  * **params** ( _kwargs_ )  (Optional) keyword-argument form for parameters such as urid, first_name, last_name, etc.

Returns

    

JSON dict of the response generated by the API

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    >>> response_json = client.query_email_and_ip_address('test@example.com', '209.85.220.41')
    

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    >>> response_json = client.query_email_and_ip_address('test@example.com', '209.85.220.41',
    ...     urid='My record ID for test@example.com and 209.85.220.41')
    

`query_ip_address`( _ip_ , _**params_ )

    

Query a risk score information for the provided IP address.

Parameters

    

  * **ip** ( _str_ )  RFC791-compliant IP

  * **params** ( _kwargs_ )  (Optional) keyword-argument form for parameters such as urid, first_name, last_name, etc.

Returns

    

JSON dict of the response generated by the API

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    >>> response_json = client.query_ip_address('209.85.220.41')
    

`remove_flag`( _query_ )

    

Unflag an email address that was marked as good or fraud previously.

Parameters

    

**query** ( _str_ )  Email to be flagged

Returns

    

JSON dict of the confirmation response generated by the API

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('My account SID', 'My auth token', sandbox=True)
    >>> response_json = client.remove_flag('test@example.com')
    

`request`( _endpoint_ , _**params_ )

    

Base method to generate requests for the Emailage validator and flagging APIs

Parameters

    

  * **endpoint** ( _str_ )  API endpoint to send the request (  | /flag )

  * **params** ( _kwargs_ )  keyword-argument list of parameters to send with the request

Returns

    

JSON dict of the response generated by the API

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('consumer_secret', 'consumer_token')
    >>> response = client.request('/flag', email='user20180830001@domain20180830001.com', flag='good')
    >>> response['query']['email']
    u'user20180830001%40domain20180830001.com'
    

`set_api_domain`( _domain_ , _tls_version= <_SSLMethod.PROTOCOL_TLSv1_2: 5>_)

    

Explicitly set the API domain to use for a session of the client, typically
used in testing scenarios

Parameters

    

  * **domain** (str see :class: ApiDomains)  API domain to use for the session

  * **tls_version** (see :class: TlsVersions)  (Optional) Uses TLS version 1.2 by default (TlsVersions.TLSv1_2 | TlsVersions.TLSv1_1)

Returns

    

None

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> from emailage.client import ApiDomains
    >>> client = EmailageClient('consumer_secret', 'consumer_token')
    >>> client.set_api_domain(ApiDomains.sandbox)
    >>> client.domain
    'https://sandbox.emailage.com'
    

Example

    
    
    
    >>> from emailage.client import EmailageClient
    >>> client = EmailageClient('consumer_secret', 'consumer_token')
    >>> client.set_api_domain('https://testing.emailage.com')
    >>> client.domain
    'https://testing.emailage.com'
    

`set_credentials`( _secret_ , _token_ )

    

Explicitly set the authentication credentials to be used when generating a
request in the current session. Useful when you want to change credentials
after initial creation of the client.

Parameters

    

  * **secret**  Consumer secret, e.g. SID or API key

  * **token**  Consumer token

Returns

    

None

`set_http_method`( _http_method_ )

    

Explicitly set the Http method (GET or POST) through which you will be sending
the request. This method will be used for any future calls made with this
instance of the client until another method is specified

Parameters

    

**http_method** (str see :class: HttpMethods)  HttpMethod to use for sending
requests

Returns

    

None

Example

    
    
    
    >>> from emailage.client import EmailageClient, HttpMethods
    >>> client = EmailageClient('consumer_secret', 'consumer_token')
    >>> client.set_http_method(HttpMethods.POST)
    >>> client.http_method
    'POST'
    

### _class_ `emailage.client.ApiDomains`

    

API URLs for the specified domains


### _class_ `emailage.client.HttpMethods`
  

HttpMethod constants to pass to the client


### _class_ `emailage.client.TlsVersions`


An enumeration of the TLS versions supported by the Emailage API


## _module_ `emailage.signature`

---
##### `emailage.signature.create`( _method_ , _url_ , _params_ , _hmac_key_ )

    

Generates the OAuth1.0 signature used as the value for the query string
parameter oauth_signature

Parameters

    

  * **method** ( _str_ )  HTTP method that will be used to send the request ( GET | POST )

  * **url** ( _str_ )  API domain and endpoint up to the ?

  * **params** ( _dict_ )  user-provided query string parameters and the OAuth1.0 parameters :method add_oauth_entries_to_fields_dict:

  * **hmac_key** ( _str_ )  for Emailage users, this is your consumer token with an & (ampersand) appended to the end

Returns

    

str value used for oauth_signature

Example

    
    
    
    >>> from emailage.signature import add_oauth_entries_to_fields_dict, create
    >>> your_api_key = 'SOME_KEY'
    >>> your_hmac_key = 'SOME_SECRET' + '&'
    >>> api_url = 'https://sandbox.emailage.com/emailagevalidator/'
    >>> query_params = { 'query': 'user.you.are.validating@gmail.com', 'user_email': 'admin@yourcompany.com' }
    >>> query_params = add_oauth_entries_to_fields_dict(your_api_key, query_params)
    >>> query_params['oauth_signature'] = create('GET', api_url, query_params, your_hmac_key)
    


(C)2018, Emailage Dev Team. | Powered by Sphinx 2.2.0 & Alabaster 0.7.12 |
Page source


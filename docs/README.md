[logo]: https://www.emailage.com/wp-content/uploads/2018/01/logo-dark.svg "Emailage Logo"

![alt text][logo](https://www.emailage.com)

The Python-language Emailage&#8482; API client helps companies integrate with our highly efficient fraud risk and
scoring system. By calling our API endpoints and simply passing us an email
and/or IP Address, companies will be provided with real-time risk scoring
assessments based around machine learning and proprietary algorithms that
evolve with new fraud trends.

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

### Query risk score information for the provided email address, IP address, or a combination

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
```eval_rst
.. py:module:: emailage.client
.. autoclass:: EmailageClient
   :members:
.. autoclass:: ApiDomains
   :undoc-members:
.. autoclass:: HttpMethods
   :undoc-members:
.. autoclass:: TlsVersions
   :undoc-members:
   
.. py:module:: emailage.signature
.. autofunction:: create
```
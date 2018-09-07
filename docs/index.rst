.. Emailage API Python Client documentation master file, created by
   sphinx-quickstart on Thu Aug 30 12:02:59 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

|alt text|\ (https://www.emailage.com)

The Python-language Emailage™ API client helps companies integrate with our highly efficient fraud risk and scoring system.
By calling our API endpoints and simply passing us an email and/or IP Address, companies will be provided with real-time risk scoring assessments based around machine learning and proprietary algorithms that evolve with new fraud trends.


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Quickstart Guide
~~~~~~~~~~~~~~~~

Requirements
------------

-  Python 2.7+ or 3.3+

Installation
------------

Emailage can be installed with pip:

::

    $ pip install emailage-official

or directly from the source code:

::

    $ git clone https://github.com/emailage/Emailage_Python.git
    $ cd Emailage_Python
    $ python setup.py install

Typical usage
~~~~~~~~~~~~~

Instantiate a client


.. code:: python

    from emailage.client import EmailageClient
    # For a production server
    emailage = EmailageClient('My account SID', 'My auth token')
    # ... or for a sandbox
    emailage = EmailageClient('My account SID', 'My auth token', sandbox=True)

Query risk score information for the provided email address, IP address, or a combination
-----------------------------------------------------------------------------------------

.. code:: python

    # For an email address
    emailage.query('test@example.com')
    # For an IP address
    emailage.query('127.0.0.1')
    # For a combination. Please note the order
    emailage.query(('test@example.com', '127.0.0.1'))
    # Pass a User Defined Record ID (URID).
    # Can be used when you want to add an identifier for a query.
    # The identifier will be displayed in the result.
    emailage.query('test@example.com', urid='My record ID for test@example.com')

For ease of use, explictly-named methods are provided as well.

.. code:: python

    # For an email address
    emailage.query_email('test@example.com')
    # For an IP address
    emailage.query_ip_address('127.0.0.1')
    # For a combination. Please note the order
    emailage.query_email_and_ip_address('test@example.com', '127.0.0.1')
    # Pass a User Defined Record ID
    emailage.query_email_and_ip_address('test@example.com', '127.0.0.1', urid='My record ID for test@example.com and 127.0.0.1')


Mark an email address as fraud, good, or neutral
------------------------------------------------

You may report that you have found that an email address is good, is associated with fraud, or neither (neutral).

The call to flag an email address as fraud _must_ be accompanied by the fraud reason ID.
The IDs and descriptions are enumerated below:

| 1 - Card Not Present Fraud
| 2 - Customer Dispute (Chargeback)
| 3 - First Party Fraud
| 4 - First Payment Default
| 5 - Identify Theft (Fraud Application)
| 6 - Identify Theft (Account Take Over)
| 7 - Suspected Fraud (Not Confirmed)
| 8 - Synthetic ID
| 9 - Other

.. code:: python

    # Mark an email address as fraud because of Synthetic ID.
    emailage.flag('fraud', 'test@example.com', 8)
    emailage.flag_as_fraud('test@example.com', 8)
    # Mark an email address as good.
    emailage.flag('good', 'test@example.com')
    emailage.flag_as_good('test@example.com')
    # Unflag an email address that was previously marked as good or fraud.
    emailage.flag('neutral', 'test@example.com')
    emailage.flag_as_neutral('test@example.com')

Troubleshooting


Client API reference
~~~~~~~~~~~~~~~~~~~~

.. py:module:: client
.. autoclass:: TlsVersions
    :undoc-members:
.. autoclass:: ApiDomains
    :undoc-members:
.. autoclass:: EmailageClient
    :members:

.. py:module:: signature
.. autofunction:: add_oauth_entries_to_fields_dict

.. autofunction:: create


.. |alt text| image:: https://www.emailage.com/wp-content/uploads/2018/01/logo-dark.svg
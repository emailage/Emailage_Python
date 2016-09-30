[logo]: https://emailage.com/Content/Images/logo.svg "Emailage Logo"

![alt text][logo](https://www.emailage.com)

The Emailage&#8482; API is organized around REST (Representational State Transfer). The API was built to help companies integrate with our highly efficient fraud risk and scoring system. By calling our API endpoints and simply passing us an email and/or IP Address, companies will be provided with real-time risk scoring assessments based around machine learning and proprietary algorithms that evolve with new fraud trends.

## Getting Started

### Requirements

* Python 2.7+ or 3.3+

### Installation

Emailage can be installed with pip:

```
$ pip install emailage-official
```

or directly from the source code:

```
$ git clone https://github.com/emailage/Emailage_Python.git
$ cd Emailage_Python
$ python setup.py install
```

## Usage

Instantiate a client
```python
from emailage.client import EmailageClient
# For a production server
emailage = EmailageClient('My account SID', 'My auth token')
# ... or for a sandbox
emailage = EmailageClient('My account SID', 'My auth token', sandbox=True)
```

Query a risk score information for the provided email address, IP address, or a combination
```python
# For an email address
emailage.query('test@example.com')
# For an IP address
emailage.query('127.0.0.1')
# For a combination. Please note the order
emailage.query(('test@example.com', '127.0.0.1'))
# Pass a User Defined Record ID.
# Can be used when you want to add an identifier for a query.
# The identifier will be displayed in the result.
emailage.query('test@example.com', urid='My record ID for test@example.com')
```
Explicit methods produce the same request while validating format of the arguments passed
```python
# For an email address
emailage.query_email('test@example.com')
# For an IP address
emailage.query_ip_address('127.0.0.1')
# For a combination. Please note the order
emailage.query_email_and_ip_address('test@example.com', '127.0.0.1')
# Pass a User Defined Record ID
emailage.query_email_and_ip_address('test@example.com', '127.0.0.1', urid='My record ID for test@example.com and 127.0.0.1')
```

Mark an email address as fraud, good, or neutral.  
All the listed forms are possible.  
When you mark something as fraud, don't forget to pass a fraud code number from this list:  
1 - Card Not Present Fraud  
2 - Customer Dispute (Chargeback)  
3 - First Party Fraud  
4 - First Payment Default  
5 - Identify Theft (Fraud Application)  
6 - Identify Theft (Account Take Over)  
7 - Suspected Fraud (Not Confirmed)  
8 - Synthetic ID  
9 - Other

```python
# Mark an email address as fraud because of Synthetic ID.
emailage.flag('fraud', 'test@example.com', 8)
emailage.flag_as_fraud('test@example.com', 8)
# Mark an email address as good.
emailage.flag('good', 'test@example.com')
emailage.flag_as_good('test@example.com')
# Unflag an email address that was previously marked as good or fraud.
emailage.flag('neutral', 'test@example.com')
emailage.remove_flag('test@example.com')
```

### Exceptions

This gem can throw exceptions on any of the following issues:

1. When Requests has an issue, like not being able to connect from your server to Emailage API,
2. When bad formatted JSON is received,
3. When an incorrect email or IP address is passed to a flagging or explicitly querying method.

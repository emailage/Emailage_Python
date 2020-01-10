# Revision History

## 1.2.0 (10 January 2020)

- HTTP verb for requests is a parameter to `__init__`, defaults to GET
- Request timeout can be specified as parameter to `__init__`
- UTF-8 characters may be sent via the POST request

## 1.1.6 (14 December 2018)

 - Fix choice of URL encoding function for Python 2.7 users


## 1.1.4 (17 September 2018)

 - Corrected IPv4 validation Regex to allow 0s in octets 2,3,4

## 1.1.0 (30 August 2018)

 - Corrected bug in the URL encoding of spaces
 - Significantly expanded documentation of signature functions
 - Extracted all OAuth signature generation logic from request generation into the signature module
 - Explicit decoding of API response bytes removes the need to run a Regex over the response

## 1.0.2 (30 October 2017)

 - Corrected the validation of IPv4 and IPv6 IP addresses
 - Added an optional parameter to specify TLS 1.1 or 1.2 on the initialization of EmailageClient

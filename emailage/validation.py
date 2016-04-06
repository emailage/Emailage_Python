"""A module for arguments validation"""

import re


def assert_email(email):
    if not re.match(r'^[^@\s]+@([^@\s]+\.)+[^@\s]+$', email):
        raise ValueError('{} is not a valid email address.'.format(email))
      
def assert_ip(ip):
    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
        raise ValueError('{} is not a valid IP address.'.format(ip))

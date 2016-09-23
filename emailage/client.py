"""OAuth1 module written according to http://oauth.net/core/1.0/#signing_process"""

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from uuid import uuid4
import json
import time
import re
import ssl

from emailage import signature, validation


class EmailageClient:
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
        """Transport adapter that allows us to use TLS v1.2."""

        def init_poolmanager(self, connections, maxsize, block=False):
            self.poolmanager = PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLSv1_2)
                
    
    def __init__(self, secret, token, sandbox=False):
        """Args:
            secret   (str): Consumer secret, e.g. SID or API key.
            token    (str): Consumer OAuth token.
            sandbox (bool): Whether to use a sandbox instead of a production server.
                Ensure the according secret and token are supplied.
                
        Note:
            HMAC key is created according to Emailage docs rather than OAuth1 spec.
        """
        self.secret, self.token, self.sandbox = secret, token, sandbox
        self.hmac_key = token + '&'
        self.session = Session()
        self.domain = 'https://{}.emailage.com'.format(self.sandbox and 'sandbox' or 'api')
        self.session.mount(self.domain, EmailageClient.Adapter())
        
    
    def request(self, endpoint, **params):
        """Basic request method utilized by #query and #flag.
        
        Args:
            endpoint (str): Currently, either an empty string or "/flag".
            **params: Non-general GET request params.
            
        Returns:
            dict: Original Emailage API's JSON body.
        """
        url = self.domain + '/emailagevalidator' + endpoint + '/'
        params = dict(
            format = 'json', 
            oauth_consumer_key = self.secret,
            oauth_nonce = uuid4(),
            oauth_signature_method = 'HMAC-SHA1',
            oauth_timestamp = int(time.time()),
            oauth_version = 1.0,
            **params
        )
        params['oauth_signature'] = signature.create('GET', url, params, self.hmac_key)
      
        res = self.session.get(url, params=params)
      
        # For whatever reason Emailage dispatches JSON with unreadable symbols at the start, like \xEF\xBB\xBF.
        json_data = re.sub(r'^[^{]+', '', res.text)
        return json.loads(json_data)
    
    
    def query(self, query, **params):
        """Query a risk score information for the provided email address, IP address, or a combination.
        
        Args:
            query (str | (str, str)): Email, IP, or both.
        
        Keyword Args:
            urid (str): User Defined Record ID.
                Can be used when you want to add an identifier for a query.
                The identifier will be displayed in the result.
            **: Extra request params as in API documentation.
        """
        if type(query) is tuple:   query = '+'.join(query)
        params['query'] = query
        return self.request('', **params)
    
    def query_email(self, email, **params):
        """Query a risk score information for the provided email address.
        This method differs from #query in that it ensures that the string supplied is in rfc2822 format.
        
        Args:
            email (str)
            **params: keywords arguments for #query
        """
        validation.assert_email(email)
        return self.query(email, **params)
    
    def query_ip_address(self, ip, **params):
        """Query a risk score information for the provided IP address.
        This method differs from #query in that it ensures that the string supplied is in rfc791 format.
        
        Args:
            ip (str)
            **params: keywords arguments for #query
        """
        validation.assert_ip(ip)
        return self.query(ip, **params)
    
    def query_email_and_ip_address(self, email, ip, **params):
        """Query a risk score information for the provided combination of an Email and IP address.
        This method differs from #query in that it ensures that the strings supplied are in rfc2822 and rfc791 formats.
        
        Args:
            email (str)
            ip    (str)
            **params: keywords arguments for #query
        """
        validation.assert_email(email)
        validation.assert_ip(ip)
        return self.query((email, ip), **params)
    
    
    def flag(self, flag, query, fraud_code=None):
        """Mark an email address as fraud, good, or neutral.
        
        Args:
            flag       (str): Either fraud, neutral, or good.
            query      (str): Email to be flagged.
            fraud_code (int): Reason why the email is considered fraud. ID of the one of FRAUD_CODES options.
                Required only if you flag something as fraud.
                See emailage.Client.FRAUD_CODES for the list of available reasons and their IDs.
        """
    
        flags = ['fraud', 'neutral', 'good']
        if flag not in flags:
            raise ValueError("flag must be one of {}. {} is given.".format(', '.join(flags), flag))

        validation.assert_email(query)
        
        params = dict(flag=flag, query=query)

        if flag == 'fraud':
            codes = self.FRAUD_CODES
            if type(fraud_code) is not int:
                raise ValueError("fraud_code must be an integer from 1 to {} corresponding to {}. {} is given.".format(len(codes), ', '.join(codes.values()), fraud_code))
            if fraud_code not in range(1, len(codes) + 1):
                fraud_code = 9
            params['fraudcodeID'] = fraud_code

        return self.request('/flag', **params)
    
    def flag_as_fraud(self, query, fraud_code):
        """Mark an email address as fraud.
        
        Args:
            query      (str): Email to be flagged.
            fraud_code (int): Reason why the email is considered fraud. ID of the one of FRAUD_CODES options.
                Required only if you flag something as fraud.
                See emailage.client.EmailageClient.FRAUD_CODES for the list of available reasons and their IDs.
        """
        return self.flag('fraud', query, fraud_code)
    
    def flag_as_good(self, query):
        """Mark an email address as good.
        
        Args:
            query (str): Email to be flagged.
        """
        return self.flag('good', query)
    
    def remove_flag(self, query):
        """Unflag an email address that was marked as good or fraud previously.
        
        Args:
            query (str): Email to be unflagged.
        """
        return self.flag('neutral', query)

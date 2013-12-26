import time
import base64
import random
import urllib
import urlparse
import hmac
import hashlib
from requests.auth import AuthBase


class TwitterSingleOAuth(AuthBase):
    '''Creates an authorization header for a single user Twitter Oauth
    request. Three-legged auth is not supported.'''
    def __init__(self, ck=None, cs=None, at=None, ats=None):
        self.consumer_key = ck
        self.consumer_secret = cs
        self.access_token = at
        self.access_token_secret = ats
        self.__nonce = None
        self.__time = None

    def __call__(self, r):
        '''Return the authorization header needed.'''
        self.__base_url = self.__get_base_url(r.url)
        self.__body = self.__get_body_params(r.body)
        self.__query = self.__get_query_params(r.url)

        r.headers['Authorization'] = self.__generate_auth_string(r)
        return r

    def __enc(self, string):
        encoded_str = urllib.quote(string, safe='')
        return encoded_str.replace('+', '%20').replace('%7E', '~')

    def __get_nonce(self, length=32):
        n = ''
        for i in range(length):
            n += random.choice('0123456789ABCDEF')

        return n

    def __get_base_url(self, url):
        url = url.split('?')

        return url[0]

    def __get_query_params(self, url):
        q = {}
        query = urlparse.urlparse(url).query

        if query != '':
            for param in query.split('&'):
                key, val = param.split('=')
                q[key] = val

        return q

    def __get_body_params(self, body):
        b = {}

        if body is not None:
            body = body.replace('+', ' ')
            body = urllib.unquote(body)
            for p in body.split('&'):
                key, val = p.split('=')
                b[key] = val

        return b

    def __calculate_signature(self, r):
        base = self.__generate_base_string(r)
        key = self.__generate_signing_key()
        signature = hmac.new(key, base, hashlib.sha1)

        return base64.b64encode(signature.digest())

    def __generate_base_string(self, r):
        base = r.method.upper() + '&'

        base += self.__enc(self.__base_url) + '&'
        base += self.__enc(self.__generate_parameter_string(r))

        return base

    def __generate_parameter_string(self, r):
        p = {}
        p['oauth_consumer_key'] = self.__enc(self.consumer_key)
        p['oauth_nonce'] = self.__enc(self.__nonce)
        p['oauth_signature_method'] = 'HMAC-SHA1'
        p['oauth_timestamp'] = self.__time
        p['oauth_token'] = self.__enc(self.access_token)
        p['oauth_version'] = '1.0'

        for k, v in self.__query.iteritems():
            p[self.__enc(k)] = self.__enc(v)

        for k, v in self.__body.iteritems():
            p[self.__enc(k)] = self.__enc(v)

        pstr = '&'.join(['{0}={1}'.format(k, p[k]) for k in sorted(p)])

        return pstr

    def __generate_signing_key(self):
        key = self.__enc(self.consumer_secret)
        key += '&'
        key += self.__enc(self.access_token_secret)

        return key

    def __generate_auth_string(self, r):
        self.__nonce = self.__get_nonce()
        self.__time = int(time.time())
        a = 'OAuth '
        a += 'oauth_consumer_key="{0}", '.format(self.__enc(self.consumer_key))
        a += 'oauth_nonce="{0}", '.format(self.__enc(self.__nonce))
        a += 'oauth_signature="{0}", '.format(self.__enc(self.__calculate_signature(r)))
        a += 'oauth_signature_method="HMAC-SHA1", '
        a += 'oauth_timestamp="{0}", '.format(self.__time)
        a += 'oauth_token="{0}", '.format(self.__enc(self.access_token))
        a += 'oauth_version="1.0"'

        return a

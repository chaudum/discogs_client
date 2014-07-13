# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

__version_info__ = (1,1,1)
__version__ = '.'.join([str(p) for p in __version_info__])

import os
import json
import urllib3
import requests
from collections import defaultdict
from .exceptions import *

user_agent = None

class APIBase(object):

    VERSION = (2,0)
    API_HOST = 'api.discogs.com'
    API_PROTOCOL = 'http'

    USER_AGENT = None

    http = urllib3.PoolManager()
    _headers = {'Accept-Encoding': 'gzip, deflate'}

    def __init__(self):
        assert self.USER_AGENT

    @property
    def headers(self):
        self._headers['User-Agent'] = self.USER_AGENT
        return self._headers

    @property
    def version(self):
        return '.'.join([unicode(v) for v in self.VERSION])

    @property
    def host(self):
        return u'{0}://{1}'.format(self.API_PROTOCOL, self.API_HOST)

    def _request(self, url, method='GET'):
        return self.http.request(method, url, headers=self.headers)

    def _load(self, url):
        r = self._request(url)
        if r.status == 200:
            try:
                data = json.loads(r.data)
            except (ValueError, TypeError) as e:
                print(e)
            else:
                return data
        else:
            print(r.status)
        return None

def api_set_user_agent(ua):
    APIBase.USER_AGENT = ua



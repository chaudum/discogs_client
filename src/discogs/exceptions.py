# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

import httplib


class DiscogsAPIError(Exception):
    """Root Exception class for Discogs API errors."""
    pass


class UserAgentError(DiscogsAPIError):
    """Exception class for User-Agent problems."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class HTTPError(DiscogsAPIError):
    """Exception class for HTTP(lib) errors."""
    def __init__(self, code):
        self.code = code
        self.msg = httplib.responses[self.code]

    def __str__(self):
        return "HTTP status %i: %s." % (self.code, self.msg)


class PaginationError(DiscogsAPIError):
    """Exception class for issues with paginated requests."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

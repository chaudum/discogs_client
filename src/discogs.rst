=====================
Discogs Python Client
=====================

    >>> from pprint import pprint

All objects are derived from the APIBase class.
The APIBase is an abstract class that holds information about the host,
protocol, version and other global stuff.

    >>> from discogs.client import APIBase

    >>> api = APIBase()
    Traceback (most recent call last):
    ...
        assert self.USER_AGENT
    AssertionError

By default the API base does not specify its own user agent. Since the Discogs
API does require a user agent string, that preferably follows ``RFC 1945``,
we need to set it with the ``api_set_user_agent`` method::

    >>> from discogs.client import api_set_user_agent

    >>> api_set_user_agent('DiscogsTestClient/1.0 +http://discogs.com')

    >>> api = APIBase()
    >>> api
    <discogs.client.APIBase object at 0x...>

    >>> api.version
    u'2.0'

    >>> api.host
    u'http://api.discogs.com'

    >>> api.headers
    {'Accept-Encoding': 'gzip, deflate',
     'User-Agent': 'DiscogsTestClient/1.0 +http://discogs.com'}

    >>> api.http
    <urllib3.poolmanager.PoolManager object at 0x...>


Resources
=========

Database
--------

**Artist**

The Artist resource represents a person in the Discogs database
who contributed to a Release in some capacity.

`Source <http://www.discogs.com/developers/resources/database/artist.html>`_

    >>> from discogs.resources.database import Artist

    >>> artist = Artist(45)
    >>> artist
    <Artist 45>

    >>> print(artist.id)
    None

    >>> artist.get()

    >>> artist.id
    45

    >>> artist.data['id']
    45

    >>> artist.data['id'] == artist.id
    True

    >>> artist.name
    u'Aphex Twin'

    >>> artist.data['name'] == artist.name
    True

    >>> artist.resource_url
    u'http://api.discogs.com/artists/45'

    >>> artist.uri
    u'http://www.discogs.com/artist/45-Aphex-Twin'

Release Collection::

    >>> artist.releases
    <ReleaseCollection '/artists/45/releases'>

    >>> artist.releases[0]
    <Release 258478>


**Release**

The Release resource represents a particular physical or digital object
released by one or more Artists.

`Source <http://www.discogs.com/developers/resources/database/release.html>`_.


    >>> from discogs.resources.database import Release

    >>> release = Release(258478)
    >>> release
    <Release 258478>

Fetch release::

    >>> release.get()

    >>> release.title, release.country, release.year
    (u"Oll Tolk'n' No Ding Atcheev'd", u'US', 2003)

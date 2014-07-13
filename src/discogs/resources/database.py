# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

import json
from urlparse import urlparse
from discogs.client import APIBase

class Resource(APIBase):

    class Meta:
        ident = None
        keys = ('id', 'resource_url', 'uri', 'data_quality')
        collections = ()

    def __init__(self, _id):
        # private attributes
        self._id = _id
        self._cached_data = None
        # public attributes
        self.id = None
        self.uri = None
        self.resource_url = None
        # caches
        for coll in self.Meta.collections:
            setattr(self, '_cached_{0}'.format(coll), None)


    def __str__(self):
        return '<{name} {id}>'.format(name=self.__class__.__name__,
                                      id=self._id)

    def __repr__(self):
        return self.__str__().encode('utf-8')

    @property
    def api_url(self):
        if not self._id:
            raise ProgrammingError('_id is required')
        if not self.Meta.ident:
            raise ProgrammingError('ident is required')
        return '/'.join([self.host, self.Meta.ident, str(self._id)])

    def get(self):
        self._get()

    def _get(self):
        data = self._load(self.api_url)
        if data:
            for k in self.Meta.keys:
                setattr(self, k, data.get(k))
        return data

    @property
    def data(self):
        if not self._cached_data:
            self._cached_data = self._get()
        return self._cached_data


class ResourceCollection(APIBase):

    class Meta:
        resource = Resource

    def __init__(self, url):
        ident = self.Meta.resource.Meta.ident
        assert ident
        super(ResourceCollection, self).__init__()
        self.idx = 0
        self.path = urlparse(url).path
        self._url = url
        data = self._load(url)
        self.pagination = data['pagination']
        self.data = data[ident]

    def __str__(self):
        return "<{name} '{url}'>".format(name=self.__class__.__name__,
                                         url=self.path)

    def __repr__(self):
        return self.__str__().encode('utf-8')

    def __iter__(self):
        return self

    __next__ = next

    def next(self):
        o = None
        # TODO: iterate and load pages
        if self.idx < len(self.data):
            o = self._object_at_index(self.idx)
            self.idx += 1
        else:
            raise StopIteration
        return o

    def __getitem__(self, index):
        return self._object_at_index(index)

    def _object_at_index(self, index):
        item = self.data[index]
        return self.Meta.resource(item['id'])


class Artist(Resource):
    """
    The Artist resource represents a person in the Discogs database
    who contributed to a Release in some capacity.
    http://www.discogs.com/developers/resources/database/artist.html
    """

    class Meta(Resource.Meta):
        ident = 'artists'
        keys = Resource.Meta.keys + ('name', 'realname', 'profile')
        collections = ('releases',)

    @property
    def releases(self):
        if not self._cached_releases:
            url = '/'.join([self.api_url, u'releases'])
            self._cached_releases = ReleaseCollection(url)
        return self._cached_releases


class ArtistCollection(ResourceCollection):
    """
    A collection of artists.
    """

    class Meta:
        resource = Artist


class Release(Resource):
    """
    The Release resource represents a particular physical or digital object
    released by one or more Artists.
    http://www.discogs.com/developers/resources/database/release.html
    """

    class Meta(Resource.Meta):
        ident = 'releases'
        keys = Resource.Meta.keys + \
            ('title', 'master_id', 'master_url', 'country', 'year')
        collections = ()


class ReleaseCollection(ResourceCollection):
    """
    A collection of releases.
    """

    class Meta:
        resource = Release


class Master(Resource):
    """
    The Master resource represents a set of similar Releases.
    Masters (also known as “master releases”) have a “main release”
    which is often the chronologically earliest.
    http://www.discogs.com/developers/resources/database/master.html
    """

    class Meta(Resource.Meta):
        ident = 'masters'
        keys = Resource.Meta.keys + \
            ('title', 'master_id', 'master_url', 'country', 'year')
        collections = ('versions',)

    @property
    def versions(self):
        if not self._cached_versions:
            url = '/'.join([self.api_url, u'versions'])
            self._cached_versions = ReleaseCollection(url)
        return self._cached_versions


class Label(Resource):
    """
    The Label resource represents a label, company, recording studio,
    location, or other entity involved with Artists and Releases.
    Labels were recently expanded in scope to include things that
    aren’t labels – the name is an artifact of this history.
    http://www.discogs.com/developers/resources/database/label.html
    """

    class Meta(Resource.Meta):
        ident = 'labels'
        keys = Resource.Meta.keys + ('name', 'profile')
        collections = ('releases',)

    @property
    def releases(self):
        if not self._cached_releases:
            url = '/'.join([self.api_url, u'releases'])
            self._cached_releases = ReleaseCollection(url)
        return self._cached_releases


class Image(Resource):
    pass


class Search(Resource):
    """
    The Search resource lists objects in the database that meet
    the criteria you specify.
    http://www.discogs.com/developers/resources/database/search-endpoint.html
    """
    pass
    
    def __init__(self, query, type):
        types = ('release', 'master', 'artist', 'label')
        if type not in types:
            raise ProgrammingError(u'{0} not a valid type.\n' +
            'Must be one of {1}.'.format(type, u','.join(types)))



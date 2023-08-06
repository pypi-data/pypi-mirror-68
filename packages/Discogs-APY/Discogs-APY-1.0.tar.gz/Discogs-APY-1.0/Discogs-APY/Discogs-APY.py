import requests


class Client:
    """Client object for interacting with the discogs API"""

    def __init__(self, user_token=None):
        if user_token:
            self.auth = {'token': user_token}
        else:
            raise Exception('You must provide a user token.')

    def release(self, discogs_id=None):
        """Returns an artist object from a given ID"""
        url = 'https://api.discogs.com/releases/'
        return Release(self, url, discogs_id)

    def master(self, discogs_id=None):
        """Returns a master object from a given ID"""
        url = 'https://api.discogs.com/masters/'
        return Master(self, url, discogs_id)

    def artist(self, discogs_id=None):
        """Returns an artist object from a given ID"""
        url = 'https://api.discogs.com/artists/'
        return Artist(self, url, discogs_id)

    def label(self, discogs_id=None):
        """Returns a label object from a given ID"""
        url = 'https://api.discogs.com/labels/'
        return Label(self, url, discogs_id)

    def get(self, url):
        """Sends a get request to the DiscogsAPY"""
        headers = {'User-agent': 'Wiper & True DiscogsAPY Wrapper'}
        r = requests.get(url, params=self.auth, headers=headers)
        return r.status_code, r.json()


class Field:
    """Base class for object attributes"""

    def __init__(self, class_name=None):
        self.class_name = class_name

    def __set_name__(self, owner, name):
        self.attr_key = name

    def __get__(self, instance, owner):
        return instance.fetch(self.attr_key)


class ObjectListField(Field):
    """An attribute returned as a list of API objects"""

    def __get__(self, instance, owner):
        object_list = []
        for json in super().__get__(instance, owner):
            class_type = eval(self.class_name)
            object_ = class_type(json=json)
            object_list.append(object_)
        return object_list


class APIObject:
    """Base class for API objects"""
    id = Field()
    data_quality = Field()
    images = ObjectListField(class_name='Image')
    resource_url = Field()
    uri = Field()

    def __init__(self, client=None, url=None, discogs_id=None, json=None):
        """API objects can be creating either by getting the info from discogs
        using an ID, or by manually passing in a json when creating an object
        list."""
        if discogs_id:
            status, json = client.get(f'{url}{discogs_id}')
            if status == 404:
                raise Exception(f'{discogs_id} was not found in {url}')
            self.json = json
        else:
            self.json = json

    def fetch(self, attr_key):
        """Returns a value from object json using the attribute as the key"""
        if attr_key not in self.json:
            raise KeyError(
                f'The \'{attr_key}\' attribute is not in the json dictionary')
        return self.json[attr_key]


class Release(APIObject):
    """A release object"""
    artist = Field()
    artists = ObjectListField(class_name='Artist')
    artists_sort = Field()
    catalog_number = Field()
    community = Field()
    companies = ObjectListField(class_name='Label')
    country = Field()
    date_added = Field()
    date_changed = Field()
    description = Field()
    estimated_weight = Field()
    extraartists = ObjectListField(class_name='Artist')
    format_quantity = Field()
    format = Field()
    formats = Field()
    genres = Field()
    identifiers = Field()
    labels = ObjectListField(class_name='Label')
    lowest_price = Field()
    master_id = Field()
    master = Field()
    master_url = Field()
    notes = Field()
    num_for_sale = Field()
    released = Field()
    released_formatted = Field()
    series = Field()
    stats = Field()
    status = Field()
    styles = Field()
    thumb = Field()
    thumbnail = Field()
    title = Field()
    tracklist = ObjectListField(class_name='Track')
    videos = Field()
    year = Field()

    def __repr__(self):
        return f'{self.title} - {self.resource_url}'


class Master(APIObject):
    """A master release object"""
    artists = ObjectListField(class_name='Artist')
    lowest_price = Field()
    main_release = Field()
    main_release_url = Field()
    most_recent_release = Field()
    most_recent_release_url = Field()
    num_for_sale = Field()
    styles = Field()
    title = Field()
    tracklist = ObjectListField(class_name='Track')
    versions_url = Field()
    videos = Field()

    def __repr__(self):
        return f'{self.title} - {self.resource_url}'


class Artist(APIObject):
    """An artist object"""
    active = Field()
    anv = Field()
    aliases = ObjectListField(class_name='Artist')
    members = ObjectListField(class_name='Artist')
    groups = ObjectListField(class_name='Artist')
    join = Field()
    name = Field()
    namevariations = Field()
    profile = Field()
    realname = Field()
    releases_url = Field()
    role = Field()
    tracks = Field()
    urls = Field()

    def __repr__(self):
        return f'{self.name} - {self.resource_url}'


class Label(APIObject):
    """A label object"""
    catno = Field()
    contact_info = Field()
    entity_type = Field()
    entity_type_name = Field()
    name = Field()
    parent_label = Field()
    profile = Field()
    releases_url = Field()
    sublabels = ObjectListField(class_name='Label')
    urls = Field()

    def __repr__(self):
        return f'{self.name} - {self.resource_url}'


class Track(APIObject):
    """A track object"""
    duration = Field()
    extraartists = ObjectListField(class_name='Artist')
    position = Field()
    title = Field()
    type_ = Field()

    def __repr__(self):
        return f'{self.position} - {self.title}'




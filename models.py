from uuid import uuid4

# This is meant to be something like an ORM for the feeds SQLite3 database, except
# only containing models matching the database tables to permit easy writing to
# the database, but without methods to get data back as Python objects (although
# that could easily be done.)

# The ancestor for all database model objects, not meant to be instantiated
# directly, but through its children.
class FeedsDBModel(object):
    def __init__(self, uuid=str(uuid4())):
        self._uuid = uuid

    def to_json(self):
        return dict((key.strip('_'),self.__dict__[key]) for key in self.__dict__)


class Article(FeedsDBModel):
    def __init__(
        self,
        uuid=None,
        feed_url=None,
        url=None,
        title=None,
        description=None,
        pub_date=None,
        image_url=None,
        html=None
    ):
        super().__init__()
        self._uuid = uuid
        self._feed_url = feed_url
        self._url = url
        self._title = title
        self._description = description
        self._pub_date = pub_date
        self._image_url = image_url
        self._html = html

    @property
    def uuid(self):
        return self._uuid

    @property
    def feed_url(self):
        return self._feed_url

    @property
    def url(self):
        return self._url

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def pub_date(self):
        return self._pub_date

    @property
    def image_url(self):
        return self._image_url  

    @property
    def html(self):
        return self._html
 

class Tag(FeedsDBModel):
    def __init__(self, uuid=None, tag_type=None, tags=[], feed_url=None, article_uuid=None):
        super().__init__()
        self._uuid = uuid
        self._tag_type = tag_type
        self._tags = ','.join(tags)
        self._feed_url = feed_url
        self._article_uuid = article_uuid

    @property
    def uuid(self):
        return self._uuid

    @property
    def tag_type(self):
        return self._tag_type

    @property
    def tags(self):
        return self._tags
    
    @property
    def feed_url(self):
        return self._feed_url

    @property
    def article_uuid(self):
        return self._article_uuid


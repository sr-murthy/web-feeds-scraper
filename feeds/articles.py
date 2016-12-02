class Article(object):

    def __init__(self, uuid=None, feed_url=None, url=None, title=None, description=None, pub_date=None, image_url=None, html=None):
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


class TaggedArticle(Article):

    def __init__(self, uuid=None, feed_url=None, url=None, title=None, description=None, pub_date=None, image_url=None, html=None):
        self._tags = {
            't1': [],
            't2': [],
            't3': [],
            't4': []
        }
        super.__init__(uuid, feed_url, url, title, description, pub_date, image_url, html)

    @property
    def tags(self):
        return self._tags

    @property
    def tagged(self, tag_type):
        return (
            isinstance(self._tags[tag_type], list) and 
            self._tags[tag_type] > [] and
            all(isinstance(tag, str) for tag in self._tags[tag_type])
        )

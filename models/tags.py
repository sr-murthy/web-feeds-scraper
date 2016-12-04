class Tag(object):
    def __init__(self, uuid=None, tag_type=None, tags=[], feed_url=None, article_uuid=None):
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

    def to_json(self):
    	return {
    	    'uuid':			self.uuid,
    	    'tag_type': 	self.tag_type,
    	    'tags': 		self.tags,
    	    'feed_url':		self.feed_url,
    	    'article_uuid': self.article_uuid
    	}

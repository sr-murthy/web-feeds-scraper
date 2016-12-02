class Tag(object):
    def __init__(self, uuid=None, tag_type=None, tags=[], article_uuid=None):
    	self._uuid = uuid
    	self._tag_type = tag_type
    	self._tags = tags
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
    def article_uuid(self):
    	return self._article_uuid

    def to_json(self):
    	return {
    	    'uuid':			self.uuid,
    	    'tag_type': 	self.tag_type,
    	    'tags': 		self.tags,
    	    'article_uuid': self.article_uuid
    	}

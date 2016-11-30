Article(object):

	def __init__(self, url=None, title=None, description=None, image_url=None, html=None):
		self._url = url
		self._title = title
		self._description = description
		self._image_url = image_url
		self._html = html

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
	def image_url(self):
		return self._image_url	

	@property
	def html(self):
		return self._html

	@url.setter
	def url(self, url):
		self._url = url

	@title.setter
	def title(self, title):
		self._title = title

	@description.setter
	def description(self, description):
		self._description = description

	@image_url.setter
	def image_url(self, image_url):
		self._image_url = image_url

	@html.setter
	def html(self, html):
		self._html = html


class TaggedArticle(Article):

	def __init__(self, url=None, title=None, description=None, image_url=None, html=None):
		self._tags = {
			't1': [],
			't2': [],
			't3': [],
			't4': []
		}
		super.__init__(url, title, description, image_url, html)

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

	@tags.setter
	def tags(self, tag_type, tags, replace=False):
		self._tags[tag_type].extend(tags) if not replace else self._tags[tag_type].clear().extend(tags)


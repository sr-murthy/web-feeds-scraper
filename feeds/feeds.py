class Feed(object):

	def __init__(self, feed_url=None, feed_description=None, feed_format=None, feed_articles=[]):
		self._feed_url = feed_url
		self._feed_description = feed_description
		self._feed_format = feed_format
		self._feed_articles = feed_articles

	@property
	def feed_url(self):
		return self._feed_url

	@property
	def feed_description(self):
		return self._feed_description

	@property
	def feed_format(self):
		return self._feed_format

	@property
	def feed_articles(self):
		return self._feed_articles	

	@feed_url.setter
	def feed_url(self, feed_url):
		self._feed_url = feed_url

	@feed_description.setter
	def feed_description(self, feed_description):
		self._feed_description = feed_description

	@feed_format.setter
	def feed_format(self, feed_format):
		self._feed_format = feed_format

	@feed_articles.setter
	def feed_articles(self, feed_articles, replace=False):
		self._feed_articles.extend(feed_articles) if not replace else self._feed_articles.clear().extend(feed_articles)

class RSSFeed(Feed):
	def __init__(self, feed_url=None, feed_description=None, feed_articles=[]):
		feed_format = 'RSS'
		super.__init__(feed_url, feed_description, feed_format, feed_articles)


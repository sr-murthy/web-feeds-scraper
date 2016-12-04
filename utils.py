def scrape_inner_tag(text, tag_name):
    start_tag = '<{}>'.format(tag_name)
    end_tag = '</{}>'.format(tag_name)
    start_index = text.index(start_tag) + len(start_tag)
    return text[start_index:start_index + text[start_index:].index(end_tag)]

def scrape_article_urls(feed_text):
    article_urls = []
    items = feed_text.split('<item>')
    for it in items:
        if not it.startswith('<?xml'):
            url = scrape_inner_tag(it, 'link')
            article_urls.append(url)

    return article_urls

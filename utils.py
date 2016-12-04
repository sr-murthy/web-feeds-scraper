import string

# Gets the inner markup of a symmetric SGML/XML/HTML tag, i.e. one with
# a starting and ending tag, e.g. <item> ... </item>. Does not work with
# non-symmetric tags, e.g. <meta name=... content=... />.
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

def scrape_article_meta_property(text, keyword):
    prop_values = []
    meta_lines = [
            line for line in text.split('\n')
            if line.startswith('<meta') and
            'name="{}"'.format(keyword) in line or
            'property="{}"'.format(keyword) in line
    ]
    non_alphabetics = string.whitespace + string.punctuation
    meta_lines = [meta_line.split('content="')[-1].strip(non_alphabetics) for meta_line in meta_lines]
    for meta_line in meta_lines:
        prop_values += meta_line.strip().split(',')
    prop_values.sort()
    return prop_values

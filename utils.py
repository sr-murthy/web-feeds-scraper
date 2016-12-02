def get_inner_tag(text, tag_name):
    start_tag = '<{}>'.format(tag_name)
    end_tag = '</{}>'.format(tag_name)
    start_index = text.index(start_tag) + len(start_tag)
    return text[start_index:start_index + text[start_index:].index(end_tag)]

def get_article_urls(feed_text):
    article_urls = []
    text = feed_text[::]
    while(True):
        try:
            url = get_inner_tag(get_inner_tag(text, 'item'), 'link').split('?')[0]
            article_urls.append(url)
            text = text[text.index(url):]
        except ValueError:
            break
    
    return article_urls

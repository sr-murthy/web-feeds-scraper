#!/usr/bin/env python3

import os
import requests
import sys

from multiprocessing.pool import Pool
from threading import Thread
from time import time
from uuid import uuid4

from db import FeedsDB
from feeds.feeds import RSSFeed
from feeds.articles import (
    Article,
    TaggedArticle,
)
from feeds.tags import Tag

def scrape_feed(feed_url):

    def get_article_urls(feed_text):

        def get_tag(text, tag_name):
            start_tag = '<{}>'.format(tag_name)
            end_tag = '</{}>'.format(tag_name)
            start_index = text.index(start_tag) + len(start_tag)
            return text[start_index:start_index + text[start_index:].index(end_tag)]

        article_urls = []
        text = feed_text[::]
        while(True):
            try:
                url = get_tag(get_tag(text, 'item'), 'link').split('?')[0]
                article_urls.append(url)
                text = text[text.index(url):]
            except ValueError:
                break
        
        return article_urls
    
    print('\tscraping feed : {}'.format(feed_url))
    article_urls = get_article_urls(requests.get(feed_url).text)
    db = FeedsDB()
    for url in article_urls:
        article = Article(uuid=str(uuid4()), url=url, html=requests.get(url).text)
        db.save('article', article)

if __name__ == '__main__':
    print('\n\tWelcome to the RSS feed scraper!')
    FeedsDB.setup()
    while(True):
        option = input(     
            '\n\tPlease enter a comma-separated list of RSS feed URLs to scrape ('
            'the scraper saves all articles in the feed to a local '
            'database), or type "Q" to exit.\n\n\t>> '
        )
        if not option == 'Q':
            feed_urls = [url.strip() for url in option.split(',')]
            start_time = time()
            pool = Pool(processes=len(feed_urls))
            pool.map(scrape_feed, feed_urls)
            end_time = time() - start_time
            print('Scraped {} feeds in {} seconds.'.format(len(feed_urls), end_time))
        sys.exit(0)



#!/usr/bin/env python3

import os
import requests
import sys

from multiprocessing.pool import Pool
from queue import Queue
from threading import Thread
from time import (
    sleep,
    time,
)
from uuid import uuid4

from db import FeedsDB
from feeds.feeds import RSSFeed
from feeds.articles import (
    Article,
    TaggedArticle,
)
from feeds.tags import Tag
from utils import (
    get_inner_tag,
    get_article_urls,
)

def scrape_feed(feed_url):

    def scrape_feed_article(article_url):
        print('\tSCRAPER: in article scraper thread for {}'.format(article_url))
        text = requests.get(article_url).text
        db = FeedsDB()
        article = Article(uuid=str(uuid4()), url=article_url, html=text)
        res = db.save('article', article)
        print('\tSCRAPER: saved article {}'.format(article_url))
        
    article_urls = get_article_urls(requests.get(feed_url).text)
    article_threads = []
    for article_url in article_urls:
        print('\t\tSCRAPER: scraping feed {}: saving article {} to db'.format(feed_url, article_url))
        t = Thread(target=scrape_feed_article, args=(article_url,))
        article_threads.append(t)
        t.start()

    for t in article_threads:
        t.join()

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
            print('\n\tSCRAPER: Scraped {} RSS feeds in {} seconds.'.format(len(feed_urls), end_time))
        sys.exit(0)



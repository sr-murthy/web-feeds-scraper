#!/usr/bin/env python3

import os
import requests
import sys

from multiprocessing.pool import Pool
from queue import LifoQueue
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
from utils import (
    get_article_urls,
    get_inner_tag,
)

def scrape_feed(feed_url):

    article_urls = get_article_urls(requests.get(feed_url).text)
    article_queue = LifoQueue()
    for url in article_urls:
        article_queue.put(url)

    def scrape_article():
        while not article_queue.empty():
            url = article_queue.get()
            print('\tSCRAPER:{}: saving article {}'.format(feed_url, url))
            text = requests.get(url).text
            db = FeedsDB()
            article = Article(uuid=str(uuid4()), url=url, html=text)
            db.save('article', article)
            article_queue.task_done()

    article_threads = []
    for i in range(len(article_urls)):
        t = Thread(target=scrape_article)
        t.start()
        article_threads.append(t)

    article_queue.join()
    return len(article_urls)
    
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
            total_articles = 0

            def count_articles(num):
                global total_articles
                total_articles += num

            feed_urls = [url.strip() for url in option.split(',')]
            num = len(feed_urls)
            pool = Pool(num)

            start_time = time()
            for url in feed_urls:
                pool.apply_async(scrape_feed, args=(url,), callback=count_articles)
            pool.close()
            pool.join()
            end_time = time() - start_time

            print('\n\tScraped {} articles from {} RSS feeds in {} seconds.\n'.format(total_articles, len(feed_urls), round(end_time, 3)))
        else:
            sys.exit(0)

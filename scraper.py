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
from models.articles import Article
from models.tags import Tag
from utils import (
    get_article_urls,
    get_inner_tag,
)

# This method could become part of a FeedScraper class, which is
# then initialised and used by the script main method as required.
def scrape_feed(feed_url):

    article_urls = get_article_urls(requests.get(feed_url).text)
    # LifoQueue leads to better run times than Queue (FIFO)
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
            # further work required to create and save article tags to db, using
            # the same threading model as for feed urls but inside scrape_feed
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
            # The process pool for scraping feed URLs - so each feed URL is
            # "processed" by a separate process, but inside a process the
            # article HTML content extraction, saving to the db, and potentially
            # the tagging, occurs via threads, one thread per article. On a
            # multi-core processor machine the processes could be distributed
            # over the different cores by the OS scheduler, but there is no way
            # of guaranteeing this at the code level. I considered using Redis,
            # but being unfamiliar with it, and given time constraints, I figured
            # it was simpler to use multi-processing and sub-process multi-threading
            # to get working model.
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

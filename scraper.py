#!/usr/bin/env python3

import requests
import sys
import threading

from multiprocessing import (
    current_process,
    Pool,
)
from threading import Thread
from time import (
    sleep,
    time,
)
from uuid import uuid4

from db import FeedsDB
from models import (
    Article,
    Tag,
)
from utils import scrape_article_urls

def get_article_urls(feed_url):
    print('\tSCRAPER: getting article urls for feed {}'.format(feed_url))
    return feed_url, scrape_article_urls(requests.get(feed_url).text)

def process_article(feed_url, url):
    text = requests.get(url).text
    save_article(Article(uuid=str(uuid4()), feed_url=feed_url,url=url, html=text))

def save_article(article):
    db = FeedsDB()
    db.save(article)
    tag_article(article)

def tag_article(article):
    tag_types = ['t1', 't2', 't3', 't4']
    def tag_article(article, tag_type):
        tag_json = {
            'uuid': str(uuid4()),
            'tag_type': tag_type,
            'tags': ['{} tags'.format(tag_type)],
            'feed_url': article.feed_url,
            'article_url': article.url,
            'article_uuid': article.uuid
        }
        save_tag(tag_json)
    tag_threads = dict(
        (tt,Thread(
            name='{}-{}'.format(tt, article.uuid),
            daemon=False,
            target=tag_article,
            args=(article, tt,))
        ) for tt in tag_types
    )
    for tt in tag_types[:3]:
        tag_threads[tt].start()
    for tt in tag_types[:3]:
        tag_threads[tt].join()
    while tag_threads['t1'].is_alive():
        sleep(0.01)
    tag_threads['t4'].start()
    tag_threads['t4'].join()

def save_tag(tag_json):
    tag = Tag(
        uuid=tag_json['uuid'],
        tag_type=tag_json['tag_type'],
        tags=tag_json['tags'],
        feed_url=tag_json['feed_url'],
        article_uuid=tag_json['article_uuid']
    )
    db = FeedsDB()
    db.save(tag)
    
if __name__ == '__main__':
    print('\n\tWelcome to the RSS feed scraper!')
    FeedsDB.setup()

    while(True):
        option = input(     
            '\n\tPlease enter a comma-separated list of RSS feed URLs to scrape ('
            'the scraper saves all articles in the feed to a local '
            'database), or type "Q" to exit.\n\t>> '
        )
        if not option == 'Q':
            print('\n')
            # The "global" list of article URLs built from all feed URLs
            article_urls = []
            successes = errors = 0

            def build_article_urls(url_tuple):
                feed_url = url_tuple[0]
                feed_article_urls = url_tuple[1]
                global article_urls
                article_urls += [(feed_url, article_url) for article_url in feed_article_urls]

            try:
                feed_urls = [url.strip() for url in option.split(',')]
                pool = Pool(len(feed_urls))

                for url in feed_urls:
                    pool.apply_async(get_article_urls, args=(url,), callback=build_article_urls)
                pool.close()
                pool.join()

                input_size = successes = len(article_urls)
                print('\n\tSCRAPER: {} articles to be scraped from {} RSS feeds.'.format(input_size, len(feed_urls)))
                sleep(3)

                start_time = time()                
                pool = Pool(input_size if input_size <= 150 else 150)
                for feed_url, article_url in article_urls:
                    pool.apply_async(process_article, args=(feed_url, article_url,))
                pool.close()
                pool.join()
                total_time = time() - start_time
            except Exception as e:
                print('\tSCRAPER: {}'.format(str(e)))
                errors += 1
                successes = len(article_urls) - errors
            else:
                print(
                    '\n\tSCRAPER: Scraped {}/{} articles from {} RSS feeds in {} seconds '
                    '(@ {} articles per second). {} errors encountered.\n'.
                    format(
                        successes,
                        len(article_urls),
                        len(feed_urls),
                        round(total_time, 3),
                        round(len(article_urls)/total_time, 3),
                        errors
                    )
                )
                sleep(2)
        else:
            sys.exit(0)

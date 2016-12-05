#!/usr/bin/env python3

import requests
import sys
import threading

from multiprocessing import (
    current_process,
    Pool,
)
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
from utils import (
    scrape_inner_tag,
    scrape_article_urls,
    scrape_article_meta_property,
)

def get_article_urls(feed_url):
    print('\tSCRAPER: getting article urls for feed {}'.format(feed_url))
    article_urls = [
        url for url in scrape_article_urls(requests.get(feed_url).text)
        if not url.endswith('.xml')
    ]
    return feed_url, article_urls

def save_article(feed_url, url):
    print('\tSCRAPER: {}: saving article {}'.format(current_process().name, url))
    text = requests.get(url).text
    title = scrape_inner_tag(text, 'title')
    description = pub_date = image_url = ''
    try:
       description = scrape_article_meta_property(text, 'description')[0]
    except IndexError:
        try:
            description = scrape_article_meta_property(text, 'og:description')[0]
        except IndexError:
            pass
    try:
        pub_date = scrape_article_meta_property(text, 'article:published_time')[0]
    except IndexError:
        try:
            pub_date = scrape_article_meta_property(text, 'article:published')[0]
        except IndexError:
            pass
    try:
        image_url = scrape_article_meta_property(text, 'thumbnail')[0]
    except IndexError:
        pass
    article = Article(
        uuid=str(uuid4()),
        feed_url=feed_url,
        url=url,
        html=text,
        title=title,
        description=description,
        pub_date=pub_date,
        image_url=image_url
    )
    print('\tSCRAPER: {}: saving article ({}, {})'.format(current_process().name, article.uuid, url))
    db = FeedsDB()
    db.save(article)
    tag_article(article)

def tag_article(article):
    print('\tSCRAPER: {}: tagging article ({}, {})'.format(current_process().name, article.uuid, article.url))
    tags = scrape_article_meta_property(article.html, 'keywords')
    print('\tSCRAPER: {}: found tags {} for article ({}, {})'.format(current_process().name, tags, article.uuid, article.url))
    tag = Tag(
        uuid=str(uuid4()),
        tags=','.join(tags),
        feed_url=article.feed_url,
        article_uuid=article.uuid
    )
    print('\tSCRAPER: {}: tagging article ({}, {})'.format(current_process().name, article.uuid, article.url))
    db = FeedsDB()
    db.save(tag)

# The methods above could all be bundled into a class, but for simplicity
# I have chosen to make them standalone methods.
    
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
            # Keeping count of the number of articles successfully saved
            # and tagged, and the number of general errors in the main loop.
            # Specific case exception handling has been omitted for simplicity.
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
                print('\tSCRAPER: article_urls = {}'.format(article_urls))
                input_size = successes = len(article_urls)
                print('\n\tSCRAPER: {} articles to be scraped from {} RSS feeds.'.format(input_size, len(feed_urls)))
                sleep(3)

                start_time = time()
                # A natural limit of about 150 processes was observed on the development system
                # (MacBook Air mid-2012 model with an Intel Core i5 processor with 2 physical cores
                # and 4 logical cores. A higher number of processes caused a noticeable slowing down.
                # The OS scheduler distributes the processes over the cores, which implies an
                # average of about 37.4 processes per logical core and 75 processes per physical core
                # on the development machine, assuming full throughput by the scheduler. However,
                # the processes here will become progressively more I/O-bound because they create a
                # chain of function calls that terminate in writing to the local SQLite3 database,
                # which uses reserved locks to limit more than one process writing to the database
                # at any given time. Therefore, increasing the process pool here substantially would
                # not really help, even if this were run on a system with many more physical cores.              
                pool = Pool(min(input_size, 150))
                for feed_url, article_url in article_urls:
                    pool.apply_async(save_article, args=(feed_url, article_url,))
                pool.close()
                pool.join()
                total_time = time() - start_time
            except Exception as e:
                print('\tSCRAPER: {}'.format(str(e)))
                errors += 1
                successes = len(article_urls) - errors
            finally:
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

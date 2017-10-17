# Web Feeds Scraper

A command-line client to scrape web feeds (initially RSS only, but extensible to supported feeds) and save their article HTML content (and other article attributes) to a local SQLite3 database (this could be replaced by any relational database with a suitable Python binding, with minimal change of code in the database module). The current version uses mocked tagging (mocked tagging of articles and saving dummy tag objects to the database) but this will be replaced by a fully functional tag extraction and save feature.

The database has the following simple schema:
    
    create table article (
        uuid        text primary key not null,
        feed_url    text not null,
        url         text not null,
        title       text,
        description text,
        pub_date    date,
        image_url   text,
        html        text
    );

    create table tag (
        uuid         text primary key not null,
        type         text not null,
        tags         text not null,
        feed_url     text not null,
        article_uuid text not null,
        foreign key(feed_url) references article(feed_url) on update cascade on delete cascade,
        foreign key(article_uuid) references article(uuid) on update cascade on delete cascade
    );

Example usage:

    $ ./scraper.py

    Welcome to the RSS feed scraper!

    DB does not exist, creating DB feeds.db ... 
    creating DB schema 

    Enter a comma-separated list of RSS feed URLs to scrape (the scraper saves all articles in the feed to a local database), or type "Q" to exit.

    >> http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml, http://feeds.bbci.co.uk/news/england/rss.xml?edition=uk, http://feeds.skynews.com/feeds/rss/uk.xml, http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/in_depth/uk/2001/uk_and_the_euro/rss.xml, http://www.telegraph.co.uk/sport/rss.xml, https://www.theguardian.com/uk/rss


    SCRAPER: getting article urls for feed http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml
    SCRAPER: getting article urls for feed http://feeds.bbci.co.uk/news/england/rss.xml?edition=uk
    SCRAPER: getting article urls for feed http://feeds.skynews.com/feeds/rss/uk.xml
    SCRAPER: getting article urls for feed http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/in_depth/uk/2001/uk_and_the_euro/rss.xml
    SCRAPER: getting article urls for feed http://www.telegraph.co.uk/sport/rss.xml
    SCRAPER: getting article urls for feed https://www.theguardian.com/uk/rss

    SCRAPER: 384 articles to be scraped from 6 RSS feeds.

    SCRAPER: Scraped 384/384 articles from 6 RSS feeds in 13.553 seconds (@ 28.334 articles per second). 0 errors encountered.

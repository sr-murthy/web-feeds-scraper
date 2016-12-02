# Web Feeds Scraper

A command-line client to scrape web feeds (initially RSS only, but extensible to supported feeds) and save their article HTML content (and other article attributes) to a relational database (SQLite3 in this case, but it could support any relational database). This also includes the tagging of articles and saving the tag data to the same database.

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

    creating database feeds.db ... 
    creating schema for feeds.db ... 

    Please enter a comma-separated list of RSS feed URLs to scrape (the scraper saves all articles in the feed to a local database), or type "Q" to exit.

    >> http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml, http://feeds.bbci.co.uk/news/england/rss.xml?edition=uk
    
    SCRAPER:http://feeds.bbci.co.uk/news/england/rss.xml?edition=uk: saving article http://www.bbc.co.uk/sport/basketball/38146864
    SCRAPER:http://feeds.bbci.co.uk/news/england/rss.xml?edition=uk: saving article http://www.bbc.co.uk/sport/rugby-union/38179527
    SCRAPER:http://feeds.bbci.co.uk/news/england/rss.xml?edition=uk: saving article http://www.bbc.co.uk/sport/football/38172446
    ...
    ...
    ...
    SCRAPER:http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml: saving article http://www.nytimes.com/2016/12/02/us/politics/donald-trump-transition.html
    SCRAPER:http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml: saving article http://www.nytimes.com/2016/12/01/us/politics/trumps-off-the-cuff-remarks-to-world-leaders-leave-diplomats-aghast.html
    SCRAPER:http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml: saving article http://www.nytimes.com/2016/12/01/us/politics/james-mattis-secrtary-of-defense-trump.html

    Scraped 64 articles from 2 RSS feeds in 2.194 seconds.








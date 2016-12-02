
create table article (
    uuid        text primary key not null,
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
    article_uuid text not null,
    foreign key(article_uuid) references article(uuid) on update cascade on delete cascade
);
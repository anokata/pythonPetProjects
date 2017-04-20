drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists urls;
create table urls (
  id integer primary key autoincrement,
  name text not null,
  link text not null
);

drop table if exists dirs;
create table dirs (
  id integer primary key autoincrement,
  name text not null,
  parent_id integer,
  foreign key(parent_id) references dirs(id)
);

insert into dirs (name, parent_id) values 
('main', null),
('sub dir one', 1),
('sub dir two', 1),
('sub dir three', 1),
('sub sub 1', 3),
('sub sub 2', 3);

insert into urls (name, link) values 
('google', 'http://google.com'),
('abc', 'http://abc.com'),
('cdew', 'http://123.com');

drop table if exists urls;
create table urls (
  id integer primary key autoincrement,
  name text not null,
  link text not null,
  dir_id integer not null,
  foreign key(dir_id) references dirs(id)
);

drop table if exists dirs;
create table dirs (
  id integer primary key autoincrement,
  name text not null
);

insert into dirs (name) values 
('main'),
('art'),
('trash'),
('joy');

insert into urls (name, link, dir_id) values 
('google', 'http://google.com', 3),
('abc', 'http://abc.com', 3),
('cba', 'http://abc.com', 1),
('cdew', 'http://123.com', 3);

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

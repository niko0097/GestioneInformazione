/*Esportazione db in archivio compresso*/
pg_dump -U niko GAvI | gzip > db.gz

/*Creazione user e passwd per un db in postgres*/
sudo -u postgres psql
postgres=# create database mydb;
postgres=# create user myuser with encrypted password 'mypass';
postgres=# grant all privileges on database mydb to myuser;

/*PostgresSql*/
ALTER TABLE articles
ADD COLUMN ts_title tsvector;

ALTER TABLE articles
ADD COLUMN ts_authors tsvector;

ALTER TABLE articles
ADD COLUMN ts_year tsvector;

/*Popolamento delle 2 colonne con valori stemmati e tokenizzati*/
UPDATE articles
SET ts_title = to_tsvector(title);

UPDATE articles
SET ts_authors = to_tsvector(authors);

UPDATE articles
SET ts_year = to_tsvector(year);

/*OPPURE*/
ALTER TABLE articles
ADD COLUMN ts_elements tsvector;

UPDATE articles
SET ts_elements = to_tsvector(title|| ' ' ||authors|| ' ' ||year);

/*Creazione indice*/
CREATE INDEX auth_titl_year_idx
ON articles
USING GIN(ts_title,ts_authors,ts_year);

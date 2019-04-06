BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `proceedings` (
	`mdate`	TEXT NOT NULL,
	`key`	TEXT NOT NULL UNIQUE,
	`authors`	TEXT,
	`editors`	TEXT,
	`title`	TEXT,
	`pages`	INTEGER,
	`year`	INTEGER,
	`volume`	TEXT,
	`publisher`	TEXT,
	`isbn`	TEXT,
	`ees`	TEXT,
	`url`	TEXT,
	`series`	TEXT,
	`crossref`	TEXT
);
CREATE TABLE IF NOT EXISTS `phdthesis` (
	`mdate`	TEXT NOT NULL,
	`key`	TEXT NOT NULL UNIQUE,
	`authors`	TEXT,
	`title`	TEXT,
	`pages`	INTEGER,
	`year`	INTEGER,
	`volume`	TEXT,
	`school`	TEXT,
	`note`	TEXT,
	`ees`	TEXT,
	`crossref`	TEXT
);
CREATE TABLE IF NOT EXISTS `mastersthesis` (
	`mdate`	TEXT NOT NULL,
	`key`	TEXT NOT NULL UNIQUE,
	`authors`	TEXT,
	`title`	TEXT,
	`pages`	INTEGER,
	`year`	INTEGER,
	`volume`	TEXT,
	`school`	TEXT,
	`note`	TEXT,
	`ees`	TEXT,
	`crossref`	TEXT
);
CREATE TABLE IF NOT EXISTS `inproceedings` (
	`mdate`	TEXT NOT NULL,
	`key`	TEXT NOT NULL UNIQUE,
	`authors`	TEXT,
	`title`	TEXT,
	`pages`	INTEGER,
	`year`	INTEGER,
	`volume`	TEXT,
	`journal`	TEXT,
	`number`	INTEGER,
	`ees`	TEXT,
	`url`	TEXT,
	`crossref`	TEXT
);
CREATE TABLE IF NOT EXISTS `book` (
	`mdate`	TEXT NOT NULL,
	`key`	TEXT NOT NULL UNIQUE,
	`authors`	TEXT,
	`title`	TEXT,
	`pages`	INTEGER,
	`year`	INTEGER,
	`volume`	TEXT,
	`publisher`	TEXT,
	`isbn`	TEXT,
	`ees`	TEXT,
	`series`	TEXT,
	`crossref`	TEXT
);
CREATE TABLE IF NOT EXISTS `articles` (
	`mdate`	TEXT NOT NULL,
	`key`	TEXT NOT NULL UNIQUE,
	`authors`	TEXT,
	`editors`	TEXT,
	`title`	TEXT,
	`pages`	INTEGER,
	`year`	INTEGER,
	`volume`	TEXT,
	`journal`	TEXT,
	`number`	INTEGER,
	`ees`	TEXT,
	`url`	TEXT,
	`crossref`	TEXT
);
COMMIT;

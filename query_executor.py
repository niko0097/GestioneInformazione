import sqlite3
class query_executor():

	'''CLASSE CHE IMPLEMENTA LA DIALOGAZIONE CON IL DATABASE, L HO FATTA PER MANTERE
	LE CLASSI PRINCIPALI PIU PULITE'''

	def __init__(self):
		self.connection = sqlite3.connect("progetto.db")
		self.cursor = self.connection.cursor()
		print("CONNESSIONE STABILITA")

	def execute_query(self,query):
		#print(query)
		self.cursor.execute(query)
		self.connection.commit()

	def create_table_query(self):
		global sql_for_tables
		self.cursor.executescript(sql_for_tables)
		self.connection.commit()

	def close_connection(self,connection):
		self.connection.close()


###QUI METTO LE QUERY DI CREAZIONE DELLE TABELLE

sql_for_tables = """
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
COMMIT; """


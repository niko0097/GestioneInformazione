class article():
	def __init__(self):
		self.tipo = "articles"
		self.key = ""				#1
		self.mdate = ""				#2
		self.authors = []			#3
		self.title = ""				#4
		self.pages = ""				#5
		self.year = ""				#6
		self.volume = ""			#7
		self.journal = ""			#8
		self.number = ""			#9
		self.ee = []				#10
		self.editor = []			#11
		self.url = ""				#12
		self.isbn = ""
		self.crossref = ""			#13


		##stringhe temporanee da buttare nel database
		self.query = ""
		self.autori = ""
		self.ees = ""
		self.editors = ""

	def put_on_db(self):
		self.autori = ' '.join(self.authors)
		self.editors = ' '.join(self.editor)
		self.ees = ' '.join(self.ee)

		#ridondante
		'''self.autori = self.autori.replace("'", " ")
		self.editors = self.editors.replace("'"," ")
		self.ees = self.ees.replace("'", ' ')
		self.title = self.title.replace("'", " ")
		self.journal = self.journal.replace("'", " ")
		'''

		self.query = """INSERT INTO {} VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' , '{}', '{}','{}');""".format(self.tipo, self.key, self.mdate, self.autori, self.title, self.pages, self.year, self.volume, self.journal, self.number, self.ees, self.editors, self.url, self.isbn,self.crossref)
		#print(self.query)
		return self.query

	def table(self):
		global sql_for_tables
		return sql_for_tables

sql_for_tables = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS articles (
	key	TEXT NOT NULL UNIQUE,
	mdate	TEXT NOT NULL,
	authors	TEXT,
	title	TEXT,
	pages	TEXT,
	year	TEXT,
	volume	TEXT,
	journal	TEXT,
	number	TEXT,
	ee	TEXT,
	editors	TEXT,
	url	TEXT,
	isbn	TEXT,
	crossref TEXT
);
COMMIT; """

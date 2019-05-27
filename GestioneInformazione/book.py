class book():
	def __init__(self):
		self.tipo = "book"
		self.key = ""		#1
		self.mdate = ""		#2
		self.title = ""
		self.publisher = ""
		self.year = ''
		self.editor = []	#3
		self.isbn = ""		#4
		self.authors = []	#5
		self.ee = []		#6
		self.pages = ""		#7
		self.crossref = ''  #8

		self.editors = ""
		self.autori = ""
		self.ees = ""

	def put_on_db(self):
		self.editors = ' '.join(self.editor)
		self.autori = ' '.join(self.authors)
		self.ees = ' '.join(self.ee)

		'''
		self.autori = self.autori.replace("'", " ")
		self.editors = self.editors.replace("'"," ")
		self.ees = self.ees.replace("'", ' ')
		self.title = self.title.replace("'", " ")
		'''

		self.query = """INSERT INTO {} VALUES('{}','{}','{}','{}', '{}', '{}', '{}', '{}', '{}', '{}','{}');""".format(self.tipo, self.key, self.mdate, self.title,self.publisher,self.year,self.editors, self.isbn, self.autori, self.ees, self.pages, self.crossref)
		return self.query

	def table(self):
		global sql_for_tables
		return sql_for_tables

sql_for_tables = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS book (
	key	TEXT NOT NULL UNIQUE,
	mdate	TEXT NOT NULL,
	title	TEXT,
	publisher	TEXT,
	year TEXT,
	editor	TEXT,
	isbn	TEXT,
	authors	TEXT,
	ee	TEXT,
	pages	TEXT,
	crossref TEXT

);
COMMIT; """

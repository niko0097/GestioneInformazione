class www():
	def __init__(self):
		self.tipo = "www"
		self.key = ""		#1
		self.mdate = ""		#2
		self.authors = []	#3
		self.ee = []		#4
		self.editor = []	#5
		self.crossref = ''  #6

		self.query = ""
		self.autori = ""
		self.editors = ""
		self.ees = ""

	def put_on_db(self):
		self.autori = ' '.join(self.authors)
		self.ees = ' '.join(self.ee)
		self.editors = ' '.join(self.editor)

		'''
		self.autori = self.autori.replace("'", " ")
		self.editors = self.editors.replace("'"," ")
		self.ees = self.ees.replace("'", ' ')
		'''

		self.query = """INSERT INTO {} VALUES('{}', '{}', '{}', '{}', '{}','{}');""".format(self.tipo ,self.key, self.mdate, self.autori, self.ees, self.editors,self.crossref)
		return self.query

	def table(self):
		global sql_for_tables
		return sql_for_tables

sql_for_tables = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS www (
	key	TEXT NOT NULL UNIQUE,
	mdate	TEXT NOT NULL,
	authors	TEXT,
	editors	TEXT,
	ee	TEXT,
	crossref TEXT

);
COMMIT; """

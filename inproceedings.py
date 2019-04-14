class inproceedings:
	def __init__(self):
		self.tipo = "inproceedings"
		self.key = ""				#1
		self.mdate = ""				#2
		self.authors = []			#3
		self.title = ""				#4
		self.pages = ""				#5
		self.year = ""				#6
		self.booktitle = ""			#7
		self.ee = []				#8
		self.crossref = ""			#9
		self.url = ""				#10
		self.editor = []			#11
		self.isbn = ""				#12

		##stringhe temporanee da buttare nel database
		self.query = ""
		self.autori = ""
		self.ees = ""
		self.editors = ""

	def put_on_db(self):
		self.autori = ' '.join(self.authors)
		self.ees = ' '.join(self.ee)
		self.editors = ' '.join(self.editor)

		'''
		self.autori = self.autori.replace("'", " ")
		self.editors = self.editors.replace("'"," ")
		self.ees = self.ees.replace("'", ' ')
		self.title = self.title.replace("'", " ")
		self.booktitle = self.booktitle.replace("'", " ")
		'''

		self.query = "INSERT INTO {} VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(self.tipo , self.key, self.mdate, self.autori , self.editors, self.isbn , self.title, self.pages, self.year, self.booktitle, self.ees, self.url, self.crossref)
		#print(self.query)
		return self.query

	def table(self):
		global sql_for_tables
		return sql_for_tables

sql_for_tables = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS inproceedings (
	key	TEXT NOT NULL UNIQUE,
	mdate	TEXT NOT NULL,
	authors	TEXT,
	editors	TEXT,
	isbn	TEXT,
	title	TEXT,
	pages	TEXT,
	year	TEXT,
	booktitle	TEXT,
	ee	TEXT,
	url	TEXT,
	crossref	TEXT

);
COMMIT; """

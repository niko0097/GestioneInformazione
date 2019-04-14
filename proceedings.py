class proceedings():
	def __init__(self):
		self.tipo = "proceedings"
		self.key = ""					#1
		self.mdate = ""					#2
		self.title = ""					#3
		self.editor = []				#4
		self.booktitle = ""				#5
		self.publisher = ""				#6
		self.series = ""				#7
		self.volume = ""				#8
		self.year = ""					#9
		self.isbn = ""					#10
		self.ee = []					#11
		self.url = ""					#12
		self.authors = []				#13
		self.pages = ''
		self.crossref = ''				#14

		##stringhe temporanee da buttare nel database
		self.query = ""
		self.ees = ""
		self.editors = ""
		self.autori = ""

	def put_on_db(self):
		self.autori = ' '.join(self.authors)
		self.ees = ' '.join(self.ee)
		self.editors = ' '.join(self.editor)

		'''
		self.autori = self.autori.replace("'", " ")
		self.editors = self.editors.replace("'"," ")
		self.ees = self.ees.replace("'", ' ')
		self.title = self.title.replace("'", " ")
		self.publisher = self.publisher.replace("'", " ")
		self.booktitle = self.booktitle.replace("'", " ")
		'''

		self.query = "INSERT INTO {} VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}');".format(self.tipo, self.key, self.mdate, self.autori , self.pages ,self.title, self.editors, self.booktitle, self.publisher, self.series, self.volume, self.year, self.isbn, self.ees, self.url,self.crossref)
		#print(self.query)
		return self.query

	def table(self):
		global sql_for_tables
		return sql_for_tables

sql_for_tables = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS proceedings (
	key	TEXT NOT NULL UNIQUE,
	mdate	TEXT NOT NULL,
	authors	TEXT,
	pages	TEXT,
	title	TEXT,
	editors	TEXT,
	booktitle	TEXT,
	publisher	TEXT,
	series	TEXT,
	volume	TEXT,
	year	TEXT,
	isbn	TEXT,
	ee	TEXT,
	url	TEXT,
	crossref TEXT

);
COMMIT; """

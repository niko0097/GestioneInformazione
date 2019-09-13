class mastersthesis():
	def __init__(self):
		self.tipo = "mastersthesis"
		self.key = ""				#1
		self.mdate = ""				#2
		self.authors = []			#3
		self.title = ""				#4
		self.year = ""				#5
		self.volume = ""			#6
		self.school = ""			#7
		self.ee = []				#8
		self.url = ""				#9
		self.pages = ""             #10
		self.crossref = ""          #11
		self.isbn = ""
		self.journal = ""
		self.number = ""
		self.editor = []


		self.query = ""
		self.autori = ""
		self.ees = ""

	def put_on_db(self):
		self.autori = ' '.join(self.authors)
		self.ees = ' '.join(self.ee)

		'''
        self.autori = self.autori.replace("'", " ")
		self.ees = self.ees.replace("'", " ")
		self.title = self.title.replace("'", " ")
		self.school = self.school.replace("'", " ")
        '''

		self.query = """INSERT INTO {} VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}');""".format(self.tipo, self.key, self.mdate, self.autori, self.title, self.year, self.volume, self.school, self.ees,  self.url, self.pages, self.crossref)
		#print(self.query)
		return self.query

	def table(self):
		global sql_for_tables
		return sql_for_tables

sql_for_tables = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS mastersthesis (
	key	TEXT NOT NULL UNIQUE,
    mdate	TEXT NOT NULL,
	authors	TEXT,
	title	TEXT,
	year	TEXT,
	volume	TEXT,
	school	TEXT,
	ee	    TEXT,
	url	TEXT,
    pages TEXT,
	crossref	TEXT
);
COMMIT; """

from query_executor import *

class obj():
	def __init__(self):
		self.tipo = "obj"
		self.mdate = ""				#1
		self.key = ""				#2
		self.author = []			#3
		self.authors = ""			#QUESTO VA NEL DATABASE, STRINGA CON TUTTI GLI AUTORI CONCATENATI
		self.title = ""				#4
		self.pages = ""				#5
		self.year = ""				#6
		self.volume = ""			#7
		self.journal = ""			#8
		self.number = ""			#9
		self.ee = []				#10
		self.ees = ""				#QUESTO VA NEL DATABASE, STRINGA CON TUTTI GLI EE CONCATENATI
		self.url = ""				#11
		self.editors = ""
		self.crossref = ""
		self.publisher = []			#12
		self.publishers = ""			#QUESTO VA NEL DATABASE

	def put_on_db(self,query_executor):
		self.authors = ''.join(self.author)
		self.ees = ''.join(self.ee)
		self.publishers = ''.join(self.publisher)

		self.authors = self.authors.replace("'"," ")
		self.publishers = self.publishers.replace("'", " ")

		#print(self.author)
		self.query = """INSERT INTO {} VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(self.tipo,  self.mdate,  self.key,  self.authors,  self.editors,  self.title,  self.pages,  self.year,  self.volume,  self.journal,  self.number,  self.ees,  self.url,  self.crossref)
		#print(self.query)
		query_executor.execute_query(self.query)

class articles():
	def __init__(self):
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
		self.ees = ""				#QUESTO VA NEL DATABASE, STRINA CON TUTTI GLI EE CONCATENATI
		self.url = ""				#11

	def put_on_db(self):
		for i in self.author:
			self.authors = self.authors + self.author[i]

		for i in self.ee:
			self.ees = self.ees + self.ee[i]

		self.query = "INSERT INTO articles VALUES ({},{},{},{},{},{},{},{},{},{},{});".format(self.mdate, self.key,self.authors,self.title,self.pages,self.year,self.volume,self.journal,self.number,self.ees,self.url)
		print(self.query)
		return self.query


##DEBUG
#a = articles()
#a.put_on_db()

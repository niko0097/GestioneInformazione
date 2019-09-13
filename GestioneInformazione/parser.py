'''SAX handler per il file XML.'''
import xml.sax
import time
from GestioneInformazione import inproceedings
from GestioneInformazione import proceedings
from GestioneInformazione import book
from GestioneInformazione import incollection
from GestioneInformazione import mastersthesis
from GestioneInformazione import phdthesis
from GestioneInformazione import article

import psycopg2
import sys
from time import time


def correctStr(stringa):
	stringa = stringa.replace("'", " ")
	stringa = stringa.replace('"', " ")
	stringa = stringa.replace('`', " ")
	return stringa



class DBLPHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.x = article.article()
		self.CurrentData = ''
		self.ee = []
		self.editor = []
		self.title = ''
		self.author = []
		self.year = ''
		self.publisher = ''
		self.key = ''
		self.crossref = ''
		self.url = ''
		self.volume = ""
		self.series = ""
		self.number = ""
		self.pages = ""
		self.journal = ""

		self.school = ''

		self.sub_counter = 0
		self.i_counter = 0
		self.cite_counter = 0
		self.cdrom_counter = 0
		self.sup_counter = 0
		self.space_counter = 0

		self.conn = psycopg2.connect(host="localhost",database="GAvI", user="niko", password="nana")
		self.c = self.conn.cursor()

		self.start = ''
		self.finish = ''


	'''Chiamato quando viene letto un nuovo oggetto.'''
	def startElement(self, tag, attr):
		global x
		self.CurrentData = tag
		if tag == 'inproceedings':
			x = inproceedings.inproceedings()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'incollection':
			x = incollection.incollection()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'mastersthesis':
			x = mastersthesis.mastersthesis()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'phdthesis':
			x = phdthesis.phdthesis()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'proceedings':
			x = proceedings.proceedings()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'book':
			x = book.book()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'article':
			x = article.article()
			x.key = attr['key']
			x.mdate = attr['mdate']


	'''Chiamato alla fine di un articolo.'''
	def endElement(self, tag):
		global x
		if tag == "author":
			x.authors.append(self.author)

		elif tag == "title":
			x.title = self.title

		elif tag == "year":
			x.year = self.year

		elif tag == "publisher":
			x.publisher = self.publisher

		elif tag == "crossref":
			x.crossref = self.crossref

		elif tag == "url":
			x.url = self.url

		elif tag == "editor":
			x.editor.append(self.editor)

		elif tag == "booktitle":
			x.booktitle = self.booktitle

		elif self.CurrentData == "series":
			x.series = self.series

		elif tag == "volume":
			x.volume = self.volume

		elif tag == "isbn":
			x.isbn == self.isbn

		elif tag == "number":
			x.number = self.number

		elif tag == "pages":
			x.pages == self.pages

		elif tag == "ee":
			x.ee.append(self.ee)

		elif tag == "journal":
			x.journal = self.journal

		elif tag == "school":
			x.school = self.school

		elif tag == "cdrom":
			self.cdrom_counter += 1

		elif tag == "cite":
			self.cite_counter += 1

		elif tag == "sub":
			self.sub_counter += 1

		elif tag == "i":
			self.i_counter += 1

		elif tag == "sup":
			self.sup_counter += 1

		elif tag == "":
			self.space_counter += 1

		elif tag in ['article','book','inproceedings','proceedings', 'incollection', 'mastersthesis','phdthesis']:								#CHIAMA UNA VOLTA E BASTA LA FUNZIONE DI X CHE BUTTA IL CONTENUTO SUL DATABASE(FUNZIONA QUINDI VA BENE)
			global current
			query = x.put_on_db()
			#print(query)
			try:
				self.c.execute(query)
				current += 1
				print("Processed: {}".format(current))
				#print("Query: {}\n".format(query))
				self.conn.commit()
			except (SyntaxError, RuntimeError, UnicodeError, Exception):
				f = open("error.txt",'a')
				f.write(query+"\n")
				f.close()

		self.CurrentData = ""

	'''Lettura di un articolo.'''
	def characters(self, content):
		global x
		content = correctStr(content)

		if self.CurrentData == "author":
			self.author = content

		if self.CurrentData == "title":
			self.title = content

		if self.CurrentData == "editor":
			self.editor = content

		if self.CurrentData == "booktitle":
			self.booktitle = content

		if self.CurrentData == "isbn":
			self.isbn = content

		if self.CurrentData == "ee":
			self.ee = content

		if self.CurrentData == "year":
			self.year = content

		if self.CurrentData == "publisher":
			self.publisher = content

		if self.CurrentData == "crossref":
			self.crossref = content

		if self.CurrentData == "url":
			self.url = content

		if self.CurrentData == "series":
			self.series = content

		if self.CurrentData == "volume":
			self.volume = content

		if self.CurrentData == "number":
			self.number = content

		if self.CurrentData == "pages":
			self.pages = content

		if self.CurrentData == "journal":
			self.journal = content

		if self.CurrentData == "school":
			self.school = content



	'''Start parsing of the document.'''
	def startDocument(self):
		print("Start parsing...")
		self.start = time()



	'''Chiusura di connessione e cursore alla fine del documento'''
	def endDocument(self):
		print("Finished parsing.")
		self.c.close()
		self.conn.close()

		#durata del parsing
		self.finish = time() - self.start
		m = int(self.finish /60)
		if m >= 60:
			h = m / 60
			m = m % 60
			print("Parsing took: {}h {}m".format(h,m))
		else:
			print("Parsing took: {}m.",m)



if __name__ == '__main__':
	try:
		conn = psycopg2.connect(host="localhost",database="GAvI", user="niko", password="nana")
		c = conn.cursor()

		x = article.article()
		c.execute(x.table())

		x = incollection.incollection()
		c.execute(x.table())

		x = book.book()
		c.execute(x.table())

		x = inproceedings.inproceedings()
		c.execute(x.table())

		x = proceedings.proceedings()
		c.execute(x.table())

		x = mastersthesis.mastersthesis()
		c.execute(x.table())

		x = phdthesis.phdthesis()
		c.execute(x.table())

		current = 0
		parser = xml.sax.make_parser()
		parser.setFeature(xml.sax.handler.feature_namespaces, 0)
		Handler = DBLPHandler()
		parser.setContentHandler( Handler )
		parser.parse("dblp.xml")

		c.close()
		conn.close()


	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		sys.exit(0)

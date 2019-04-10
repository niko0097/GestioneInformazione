'''SAX handler per il file XML.'''
import xml.sax
import time
from article import *
from inproceedings import *
from proceedings import *
from book import *
from incollection import *
from www import *
import sqlite3

class DBLPHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.x = article()
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

		#contatori per self.currentdata aggiuntivo
		self.sub_counter = 0
		self.i_counter = 0
		self.cite_counter = 0
		self.cdrom_counter = 0
		self.sup_counter = 0
		self.space_counter = 0

		#SQLITE
		self.conn = sqlite3.connect('progetto.db')
		self.c = self.conn.cursor()

	'''Chiamato quando viene letto un nuovo oggetto.'''
	def startElement(self, tag, attr):
		global x
		self.CurrentData = tag
		if tag == 'inproceedings':
			x = inproceedings()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'incollection':
			x = incollection()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'masterthesis':
			x = masterthesis()
			x.key = attr['key']
			x.mdate = attr['mdate']
			print("masterthesis")

		elif tag == 'www':
			x = www()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'phthesis':
			x = phthesis()
			x.key = attr['attr']
			x.mdate = attr['mdate']
			print("phthesis")

		elif tag == 'proceedings':
			x = proceedings()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'book':
			x = book()
			x.key = attr['key']
			x.mdate = attr['mdate']

		elif tag == 'article':
			x = article()
			x.key = attr['key']
			x.mdate = attr['mdate']


	'''Chiamato alla fine di un articolo.'''
	def endElement(self, tag):					#PER L'AMOR DI DIO NON CAMBIARE STA PARTE CHE FUNZIONA NON SO PERCHE'
		global x
		if self.CurrentData == "author":
			x.authors.append(self.author)

		elif self.CurrentData == "title":
			x.title = self.title

		elif self.CurrentData == "year":
			x.year = self.year

		elif self.CurrentData == "publisher":
			x.publisher = self.publisher

		elif self.CurrentData == "crossref":
			x.crossref = self.crossref

		elif self.CurrentData == "url":
			x.url = self.url

		elif self.CurrentData == "editor":
			x.editor.append(self.editor)

		elif self.CurrentData == "booktitle":
			x.booktitle = self.booktitle

		elif self.CurrentData == "series":
			x.series = self.series

		elif self.CurrentData == "volume":
			x.volume = self.volume

		elif self.CurrentData == "isbn":
			x.isbn == self.isbn

		elif self.CurrentData == "number":
			x.number = self.number

		elif self.CurrentData == "pages":
			x.pages == self.pages

		elif self.CurrentData == "ee":
			x.ee.append(self.ee)

		elif self.CurrentData == "journal":
			x.journal = self.journal

		elif self.CurrentData == "cdrom":
			self.cdrom_counter += 1

		elif self.CurrentData == "cite":
			self.cite_counter += 1

		elif self.CurrentData == "sub":
			self.sub_counter += 1

		elif self.CurrentData == "i":
			self.i_counter += 1

		elif self.CurrentData == "sup":
			self.sup_counter += 1

		elif self.CurrentData == "":
			self.space_counter += 1

		else:								#CHIAMA UNA VOLTA E BASTA LA FUNZIONE DI X CHE BUTTA IL CONTENUTO SUL DATABASE(FUNZIONA QUINDI VA BENE)
			global current
			query = x.put_on_db()
			#print(query)
			self.c.executescript(query)
			current += 1
			print("Processed: {}".format(current))

		self.CurrentData = ""

	'''Lettura di un articolo.'''
	def characters(self, content):				#NON CAMBIARE STA PARTE (funziona non so perche')
		global x
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




###########################
### CREO LE TABELLE ###
conn = sqlite3.connect('progetto.db')
c = conn.cursor()

x = article()
c.executescript(x.table())

x = incollection()
c.executescript(x.table())

x = book()
c.executescript(x.table())

x = inproceedings()
c.executescript(x.table())

x = proceedings()
c.executescript(x.table())

x = www()
c.executescript(x.table())

##########################
##########################


current = 0
# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
# override the default ContextHandler
Handler = DBLPHandler()
parser.setContentHandler( Handler )
parser.parse("dblp.xml")

conn.close()

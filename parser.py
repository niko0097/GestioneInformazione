'''SAX handler per il file XML.'''
import xml.sax
import sqlite3
from obj import *
from articles import *
from book import *
from inproceedings import *

class DBLPHandler(xml.sax.ContentHandler):

	def __init__(self):
		self.CurrentData = ''
		self.title = ''
		self.author = ''
		self.year = ''
		self.publisher = ''
		self.key = ''
		self.crossref = ''
		self.url = ''
		self.ee = ''

	'''Chiamato quando viene letto un nuovo oggetto.'''
	def startElement(self, tag, attr):
		self.CurrentData = tag

		global x
		if tag == 'book':
			#print("BOOK")
			x = book()
			x.key = attr['key']
			x.mdate = attr['mdate']

		if tag == 'inproceedings':
			#print("INPROCEEDING")
			x = inproceedings()
			x.key = attr['key']
			x.mdate = attr['mdate']

		if tag == 'phthesis':
			#print("PHTHESIS")
			x = phthesis()
			x.key = attr['key']
			x.mdate = attr['mdate']

		if tag == 'article':
			#print("ARTICLE")
			x = article()
			x.key = attr['key']
			x.mdate = attr['mdate']

		##A QUESTO PUNTO ABBIAMO X(OGGETO NON IDENTIFICATO TRA BOOK, INPROCEEDINGS,PHTHTESIS,ARTICLE) CON KEY E MDATE SETTATI

	'''Chiamato alla fine di un articolo.'''
	def endElement(self, tag):
		global counter
		global tot
		global x

		if self.CurrentData == "author":
			x.author.append(self.author)
			#print(x.author)
			#print ("Author:", self.author)

		if self.CurrentData == "title":
			x.title = self.title
			#print ("Title:", self.title)

		if self.CurrentData == "year":
			x.year = self.year
			#print ("Year:", self.year)

		if self.CurrentData == "publisher":
			x.publisher.append(self.publisher)
			#print ("Publisher:", self.publisher)

		if self.CurrentData == "crossref":
			x.crossref = self.crossref
			#print ("Crossref:", self.crossref)

		if self.CurrentData == "ee":
			x.ee.append(self.ee)

		if self.CurrentData == "url":
			x.url = self.url
			#print ("Url:", self.url)

		if tag == 'article':			##SE INCONTRA IL TAG ARTICLE, VUOL DIRE CHE L ARTICOLO E' FINITO E COMPLETO,POSSIAMO QUINDI INSERIRLO NEL DATABASE
			global conn
			counter += 1
			percentuale = counter / tot * 100
			print("{} %".format(percentuale))
			x.put_on_db(conn)

		self.CurrentData = ""

		##IN TEORIA ORA ABBIAMO TUTTI I DATI DENTRO L OGGETTO "x" QUINDI POSSIAMO CARICARLO SU DATABASE CHIAMANDO LA FUNZIONE "x.put_on_db()"

	'''Lettura di un articolo.'''
	def characters(self, content):

		if self.CurrentData == "author":
		    self.author = content

		elif self.CurrentData == "title":
			self.title = content

		elif self.CurrentData == "year":
			self.year = content

		elif self.CurrentData == "publisher":
			self.publisher = content

		elif self.CurrentData == "crossref":
			self.crossref = content

		elif self.CurrentData == "url":
			self.url = content

counter = 0
tot = 4552674
x = obj()
conn = sqlite3.connect("progetto.db")
cursor = conn.cursor()
sql = """CREATE TABLE IF NOT EXISTS `articles` (
	`mdate`	TEXT NOT NULL,
	`key`	TEXT NOT NULL UNIQUE,
	`authors`	TEXT,
	`editors`	TEXT,
	`title`	TEXT,
	`pages`	TEXT,
	`year`	TEXT,
	`volume`	TEXT,
	`journal`	TEXT,
	`number`	TEXT,
	`ees`	TEXT,
	`url`	TEXT,
	`crossref`	TEXT
);"""
cursor.execute(sql)
conn.commit()

# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
# override the default ContextHandler
Handler = DBLPHandler()
parser.setContentHandler( Handler )
parser.parse("dblp.xml")

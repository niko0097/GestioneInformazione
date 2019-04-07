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
		self.ee = ""

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
			x.author.append(self.author.replace("'", " "))

		if self.CurrentData == "title":
			x.title = self.title.replace("'", " ")

		if self.CurrentData == "year":
			x.year = self.year

		if self.CurrentData == "publisher":
			x.publisher.append(self.publisher)

		if self.CurrentData == "crossref":
			x.crossref = self.crossref

		if self.CurrentData == "ee":
			x.ee.append(self.ee)

		if self.CurrentData == "url":
			x.url = self.url

		if tag == 'article':			##SE INCONTRA IL TAG ARTICLE, VUOL DIRE CHE L ARTICOLO E' FINITO E COMPLETO,POSSIAMO QUINDI INSERIRLO NEL DATABASE
			global conn
			global query_executor
			counter += 1
			percentuale = counter / tot * 100
			print("{} %".format(percentuale))
			x.put_on_db(query_executor)

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
query_executor = query_executor()
query_executor.create_table_query()

# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
# override the default ContextHandler
Handler = DBLPHandler()
parser.setContentHandler( Handler )
parser.parse("dblp.xml")

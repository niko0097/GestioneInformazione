'''SAX handler per il file XML.'''
import xml.sax
#import sqlite3
from articles import *
from inproceedings import *
from phthesis import *

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
		self.__AllData = []	#IN QUESTO OGGETTO FINISCONO TUTTI I TIPI DI OGGETTO, OGNIUNO CON LA SUA FUNZIONE "put_to_db" CHE INSERISCE NELLA TABELLA GIUSTA I SUOI VALORI

	'''Chiamato quando viene letto un nuovo oggetto.'''
	def startElement(self, tag, attr):
		self.CurrentData = tag

		if tag == 'book':
			print("BOOK")
			x = book()
			b.key = attr['key']
			b.mdate = attr['mdate']

		if tag == 'inproceedings':
			print("INPROCEEDING")
			x = inproceedings()
			x.key = attr['key']
			x.mdate = attr['mdate']

		if tag == 'phthesis':
			print("PHTHESIS")
			x = phthesis()
			x.key = attr['key']
			x.mdate = attr['mdate']

		if tag == 'article':
			print("ARTICLE")
			x = article()
			x.key = attr['key']
			x.mdate = attr['mdate']

		##A QUESTO PUNTO ABBIAMO X(OGGETO NON IDENTIFICATO TRA BOOK, INPROCEEDINGS,PHTHTESIS,ARTICLE) CON KEY E MDATE SETTATI


	'''Chiamato alla fine di un articolo.'''
	def endElement(self, tag):
		#if self.CurrentData == "author":
			#print ("Author:", self.author)
		#elif self.CurrentData == "title":
			#print ("Title:", self.title)
		#elif self.CurrentData == "year":
			#print ("Year:", self.year)
		#elif self.CurrentData == "publisher":
			#print ("Publisher:", self.publisher)
		#elif self.CurrentData == "crossref":
			#print ("Crossref:", self.crossref)
		#elif self.CurrentData == "url":
			#print ("Url:", self.url)
		self.CurrentData = ""

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


# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
# override the default ContextHandler
Handler = DBLPHandler()
parser.setContentHandler( Handler )
parser.parse("dblp.xml")

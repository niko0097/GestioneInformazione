'''SAX handler per il file XML.'''
import xml.sax



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

    '''Chiamato quando viene letto un nuovo articolo.'''
    def startElement(self, tag, attr):
        self.CurrentData = tag
        if tag == 'article':
            print('/************************ Article ****************************/')
            key = attr['key']
            mdate = attr['mdate']
            print('key: {}   -   mdate: {}'.format(key, mdate))

    '''Chiamato alla fine di un articolo.'''
    def endElement(self, tag):
        if self.CurrentData == "author":
            print ("Author:", self.author)
        elif self.CurrentData == "title":
            print ("Title:", self.title)
        elif self.CurrentData == "year":
            print ("Year:", self.year)
        elif self.CurrentData == "publisher":
            print ("Publisher:", self.publisher)
        elif self.CurrentData == "crossref":
            print ("Crossref:", self.crossref)
        elif self.CurrentData == "url":
            print ("Url:", self.url)
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


'''# create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = MovieHandler()
   parser.setContentHandler( Handler )

   parser.parse("movies.xml")
'''

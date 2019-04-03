'''SAX handler per il file XML.'''
import xml.sax

class DBLPHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.__fields = ["title",
                            "year",
                            "key",
                            "publisher",
                            "crossref",
                            "url",
                            "ee",
                            "journal",
                            "booktitle"] #author va gestito separatamente

        self.CurrentData = ''
        self.key = ''
        self.title = ''
        self.author = []
        self.year = ''
        self.publisher = ''
        self.crossref = ''
        self.url = ''
        self.journal = ''
        self.ee = ''
        self.booktitle = ''

        self.__AllData = []


    '''Eliminazione dei caratteri che disturbano l'inserimento nel db'''
    def __correctString(self, txt):
        app = txt.replace(chr(39),'') #carattere '
        txt = app.replace(chr(34),"") #carattere "
        return txt


    '''Chiamato quando viene letto un nuovo articolo.'''
    def startElement(self, tag, attr):
        self.CurrentData = tag

        if tag == 'article' or tag == 'inproceedings':
            self.key = attr['key']



    '''Chiamato alla fine di un articolo.'''
    def endElement(self, tag):
        if tag == 'article' or tag == 'inproceedings':

            '''creazione del dict con le info prese dall'articolo'''
            appoggio = {x:getattr(self,x)  \
                for x in self.__fields+['author']  \
                if getattr(self,x) != ''}

            self.__AllData.append(appoggio)

            '''Svuoto i vari campi.'''
            self.author = []
            for x in self.__fields:
                setattr(self,x,'')

        self.CurrentData = ""



    def endElement(self, tag):
        print('Done parsing')

        

    '''Lettura di un articolo.'''
    def characters(self, content):
        if self.CurrentData in self.__fields:
            setattr(self,self.CurrentData,self.__correctString(content))

        elif self.CurrentData == 'author':
            self.author.append(self.__correctString(content))


    '''Restituzione della lista.'''
    @property
    def data(self):
        return self.__AllData

'''# create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = MovieHandler()
   parser.setContentHandler( Handler )

   parser.parse("movies.xml")
'''

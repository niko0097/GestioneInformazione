from .book import book

class proceedings(book):
    def __init__(self):
        super().__init__(self)
        self.fields = ['title','pages','year','volume','publisher','isbn','url','series','crossref']
        self.tipo = 'proceedings'
        
        self.editor = []
        self.editors = ''

    def put_on_db(self):
        for i in self.author:
            self.authors = self.authors+ ", " + self.author[i]

        for i in self.ee:
            self.ees = self.ees + ", " +  self.ee[i]

        for i in self.editor:
            self.editors = self.editors + ", " + self.editor[i]

        self.query = "INSERT INTO {} VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{});".format(
                                        self.tipo,
                                        self.mdate,
                                        self.key,
                                        self.authors,
                                        self.editors,
                                        self.title,
                                        self.pages,
                                        self.year,
                                        self.volume,
                                        self.publisher,
                                        self.isbn,
                                        self.ees,
                                        self.url,
                                        self.series,
                                        self.crossref)
        print(self.query)
        return self.query

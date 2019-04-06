from .article import article

class book(article):
    def __init__(self):
        super().__init__(self)
        self.fields = ['title','pages','year','volume','publisher','isbn','series','crossref']

        self.tipo ='book'
        self.publisher = ''
        self.isbn = ''
        self.series = ''


    def put_on_db(self):
        for i in self.author:
            self.authors = self.authors + ", " +  self.author[i]

        for i in self.ee:
            self.ees = self.ees + ", " +  self.ee[i]

        self.query = "INSERT INTO {} VALUES ({},{},{},{},{},{},{},{},{},{},{},{});".format(
                                        self.tipo,
                                        self.mdate,
                                        self.key,
                                        self.authors,
                                        self.title,
                                        self.pages,
                                        self.year,
                                        self.volume,
                                        self.publisher,
                                        self.isbn,
                                        self.ees,
                                        self.series,
                                        self.crossref)
        print(self.query)
        return self.query

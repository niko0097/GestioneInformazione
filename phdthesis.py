from .article import article

class phdthesis(article):
    def __init__(self):
        super().__init__(self)
        self.fields = ['title','year','volume','school','note','crossref']
        self.tipo = 'phdthesis'

        self.note = ''
        self.school = ''

    def put_on_db(self):
        for i in self.author:
            self.authors = self.authors + ", " +  self.author[i]

        for i in self.ee:
            self.ees = self.ees + ", " +  self.ee[i]

        self.query = "INSERT INTO {} VALUES ({},{},{},{},{},{},{},{},{},{});".format(
                                        self.tipo,
                                        self.mdate,
                                        self.key,
                                        self.authors,
                                        self.title,
                                        self.year,
                                        self.volume,
                                        self.school,
                                        self.note,
                                        self.ees,
                                        self.crossref)
        print(self.query)
        return self.query

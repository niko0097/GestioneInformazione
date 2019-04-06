class article():
    def __init__(self):
        self.fields = ['title','pages','year','volume','journal','number','url','crossref']

        self.tipo = "articles"

        self.mdate = ""
        self.key = ""
        self.author = []
        self.authors = ""
        self.title = ""
        self.pages = ""
        self.year = ""
        self.volume = ""
        self.journal = ""
        self.number = ""
        self.ee = []
        self.ees = ""
        self.url = ""
        self.crossref = ""

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
                                        self.journal,
                                        self.number,
                                        self.ees,
                                        self.url,
                                        self.crossref)
        print(self.query)
        return self.query

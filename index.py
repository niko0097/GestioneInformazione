from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os

class index():
    def __init__(self):

        self.schema = Schema(title = TEXT(stored=TRUE),
                        author = TEXT(stored=TRUE),
                        year = NUMERIC(stored=TRUE)
                        publisher = TEXT
                        key = ID(stored = TRUE),
                        crossref = ID)

        if not os.path.exists('indice'):
            os.mkdir('indice')
        create_in('indice', schema)

    def populateIndex(self):

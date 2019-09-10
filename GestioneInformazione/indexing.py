#!/usr/bin/env python3


import psycopg2


# Classe per l'indicizzazione di ogni tabella del db.
# Si presuppone che il database sia locale, che si chiami 'GAvI', lo user che vi accede sia 'niko' e la sua pw sia 'nana'.
# Questa classe si occupa di indicizzare ogni tabella sui campi 'title', 'author', e 'year', per supportare la ricerca
# su uno di questi 3 campi singolarmente, o su tutti e 3 assieme.
# A seconda della tabella, è poi necessario indicizzare un altro campo (publisher o journal) per velocizzare le ricerche
# della venue
class indexer:
    def __init__(self):
        self.tables = ['articles','book','incollection','inproceedings','mastersthesis','phdthesis','proceedings']
        self.db = 'GAvI'
        self.host = 'localhost'
        self.user = 'niko'
        self.pw = 'nana'

        self.conn = ''

    # Funzione per la creazione dell'indice su ogni tabella
    def createColIndex(self):
        # Connessione con db
        print("Starting connection...")
        conn = psycopg2.connect(host=self.host, database=self.db, user=self.user, password=self.pw)
        cur = conn.cursor()
        print("Connection established.")

        # Su ogni tabella viene creata una colonna per ogni campo di ricerca. I dati all'interno sono tsvector
        for tab in self.tables:
            query = """
                    ALTER TABLE {} ADD COLUMN ts_title tsvector;
                    ALTER TABLE {} ADD COLUMN ts_authors tsvector;
                    ALTER TABLE {} ADD COLUMN ts_year tsvector;
                    ALTER TABLE {} ADD COLUMN ts_text_all tsvector;
                    ALTER TABLE {} ADD COLUMN ts_venue_all tsvector;

                    UPDATE {} SET ts_title = to_tsvector(title);
                    UPDATE {} SET ts_authors = to_tsvector(authors);
                    UPDATE {} SET ts_year = to_tsvector(year);
                    UPDATE {} SET ts_text_all = to_tsvector(title || ' ' || authors || ' ' || year);
                    """.format(tab,tab,tab,tab,tab,tab,tab,tab,tab)

            query2 = ""
            if tab == 'articles':
                query2 = """
                        ALTER TABLE {} ADD COLUMN ts_journal tsvector;
                        UPDATE {} SET ts_journal = to_tsvector(journal);
                        UPDATE {} SET ts_venue_all = to_tsvector(title || ' ' || journal);
                        """.format(tab,tab,tab)
            elif tab in ['proceedings','book','incollection']:
                query2 = """
                        ALTER TABLE {} ADD COLUMN ts_publisher tsvector;
                        UPDATE {} SET ts_publisher = to_tsvector(publisher);
                        UPDATE {} SET ts_venue_all = to_tsvector(title || ' ' || publisher);
                        """.format(tab,tab,tab)

            try:
                print("Modifing and updating {} table...".format(tab))
                cur.execute(query)
                conn.commit()
                if query2 != '':
                    print("Still updating...")
                    cur.execute(query2)
                    conn.commit()
            except Exception as e:
                print(e)
                cur.close()
                conn.close()
                return

            # Creazione effettiva dell'indice
            if tab in ['mastersthesis','phdthesis','inproceedings']:
                query = """
                        CREATE INDEX {}_idx ON {}
                        USING GIN(ts_title,ts_authors,ts_year,ts_text_all);
                        """.format(tab,tab)
            elif tab == 'articles':
                query = """
                        CREATE INDEX {}_idx ON {}
                        USING GIN(ts_title,ts_authors,ts_year,ts_journal,ts_text_all,ts_venue_all);
                        """.format(tab,tab)
            else:
                query = """
                        CREATE INDEX {}_idx ON {}
                        USING GIN(ts_title,ts_authors,ts_year,ts_publisher,ts_text_all,ts_venue_all);
                        """.format(tab,tab)

            try:
                print("Creating index on {}...".format(tab))
                cur.execute(query)
                conn.commit()
                print("Index created.")
            except Exception as e:
                print(e)
                cur.close()
                conn.close()
                return

        print("Done.")
        cur.close()
        conn.close()

    # Funzione per l'eleiminazione dell'indice. Usare solo se assolutamente necessario.
    def deleteIdx(self):
        print("Starting connection...")
        conn = psycopg2.connect(host=self.host, database=self.db, user=self.user, password=self.pw)
        cur = conn.cursor()
        print("Connection established.")

        for tab in self.tables:
            query = """DROP INDEX IF EXISTS {}_idx;""".format(tab)
            try:
                print("Dropping index on {}...".format(tab))
                cur.execute(query)
                conn.commit()
            except Exception as e:
                print(e)
                cur.close()
                conn.close()
                return

            query = """
                    ALTER TABLE {0} DROP COLUMN IF EXISTS ts_title;
                    ALTER TABLE {0} DROP COLUMN IF EXISTS ts_authors;
                    ALTER TABLE {0} DROP COLUMN IF EXISTS ts_year;
                    ALTER TABLE {0} DROP COLUMN IF EXISTS ts_journal;
                    ALTER TABLE {0} DROP COLUMN IF EXISTS ts_publisher;
                    ALTER TABLE {0} DROP COLUMN IF EXISTS ts_text_all;
                    ALTER TABLE {0} DROP COLUMN IF EXISTS ts_venue_all;
                    """.format(tab)
            try:
                print("Deleting ts_elements on {}...".format(tab))
                cur.execute(query)
                conn.commit()
            except Exception as e:
                print(e)
                cur.close()
                conn.close()
                return
        cur.close()
        conn.close()



# Script per la creazione dell'indice da terminale. Se si lancia questo script si presuppone che si voglia creare
# l'indice E BASTA
if __name__ == '__main__':
    ind = indexer()
    ind.createColIndex()

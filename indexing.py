#!/usr/bin/env python3
'''
SCRIPT PER L'INDICIZZAZIONE DEL DB.
'''

import psycopg2

class indexer:
    def __init__(self):
        self.tables = ['articles','book','incollection','inproceedings','mastersthesis','phdthesis','proceedings']
        self.db = 'GAvI'
        self.host = 'localhost'
        self.user = 'niko'
        self.pw = 'nana'

        self.conn = ''

    def createColIndex(self):
        print("Starting connection...")
        conn = psycopg2.connect(host=self.host, database=self.db, user=self.user, password=self.pw)
        cur = conn.cursor()
        print("Connection established.")

        for tab in self.tables:
            query = """
                    ALTER TABLE {} ADD COLUMN ts_title tsvector;
                    ALTER TABLE {} ADD COLUMN ts_authors tsvector;
                    ALTER TABLE {} ADD COLUMN ts_year tsvector;

                    UPDATE {} SET ts_title = to_tsvector(title);
                    UPDATE {} SET ts_authors = to_tsvector(authors);
                    UPDATE {} SET ts_year = to_tsvector(year);
                    """.format(tab,tab,tab,tab,tab,tab)

            query2 = ""
            if tab == 'articles':
                query2 = """
                        ALTER TABLE {} ADD COLUMN ts_journal tsvector;
                        UPDATE {} SET ts_journal = to_tsvector(journal);
                        """.format(tab,tab)
            elif tab in ['proceedings','book','incollection']:
                query2 = """
                        ALTER TABLE {} ADD COLUMN ts_publisher tsvector;
                        UPDATE {} SET ts_publisher = to_tsvector(publisher);
                        """.format(tab,tab)

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

            if tab in ['mastersthesis','phdthesis','inproceedings']:
                query = """CREATE INDEX {}_idx ON {} USING GIN(ts_title,ts_authors,ts_year);""".format(tab,tab)
            elif tab == 'articles':
                query = """CREATE INDEX {}_idx ON {} USING GIN(ts_title,ts_authors,ts_year,ts_journal);""".format(tab,tab)
            else:
                query = """CREATE INDEX {}_idx ON {} USING GIN(ts_title,ts_authors,ts_year,ts_publisher);""".format(tab,tab)

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
                    ALTER TABLE {} DROP COLUMN IF EXISTS ts_title;
                    ALTER TABLE {} DROP COLUMN IF EXISTS ts_authors;
                    ALTER TABLE {} DROP COLUMN IF EXISTS ts_year;
                    ALTER TABLE {} DROP COLUMN IF EXISTS ts_journal;
                    ALTER TABLE {} DROP COLUMN IF EXISTS ts_publisher;
                    """.format(tab,tab,tab,tab,tab)
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


if __name__ == '__main__':
    #se lo lancio da python suppongo di voler solo creare un indice
    ind = indexer()
    ind.createColIndex()

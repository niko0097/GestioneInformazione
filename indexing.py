#!/usr/bin/env python3
'''
SCRIPT PER L'INDICIZZAZIONE DEL DB.
'''

import psycopg2

class indexer():
    def __init__(self):
        self.tables = ['articles','book','incollection','inproceedings','mastersthesis','phdthesis','proceedings','www']
        self.db = 'GAvI'
        self.host = 'localhost'
        self.user = 'niko'
        self.pw = 'nana'

        self.conn = ''

    def createSingleColIndex(self):
        print("Starting connection...")
        conn = psycopg2.connect(host=self.host, database=self.db, user=self.user, password=self.pw)
        cur = conn.cursor()
        print("Connection established.")

        for tab in self.tables:
            query = "ALTER TABLE {} ADD COLUMN ts_elements tsvector;".format(tab)
            try:
                print("Modifing {} table...".format(tab))
                cur.execute(query)
                conn.commit()
            except Exception as e:
                print(e)
                cur.close()
                conn.close()
                return

            if tab in ['articles','inproceedings','mastersthesis','phdthesis','proceedings']:
                query = "UPDATE {} SET ts_elements = to_tsvector(title|| ' ' ||authors|| ' ' ||year);".format(tab)
            elif tab in ['book','incollection','www']:
                query = "UPDATE {} SET ts_elements = to_tsvector(editors|| ' ' ||authors);".format(tab)

            try:
                print("Setting {} table with tsvectors...".format(tab))
                cur.execute(query)
                conn.commit()
            except Exception as e:
                print(e)
                cur.close()
                conn.close()
                return

            query = "CREATE INDEX {}_idx ON {} USING GIN(ts_elements);".format(tab,tab)
            try:
                print("Creating index on {}...".format(tab))
                cur.execute(query)
                conn.commit()
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
            query = "DROP INDEX IF EXISTS {}_idx;".format(tab)
            try:
                print("Dropping index on {}...".format(tab))
                cur.execute(query)
                conn.commit()
            except Exception as e:
                print(e)
                cur.close()
                conn.close()
                return

            query = "ALTER TABLE {} REMOVE COLUMN ts_elements;".format(tab)
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
    ind.createSingleColIndex()

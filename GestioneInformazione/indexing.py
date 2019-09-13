#!/usr/bin/env python3


import psycopg2
import sys

class indexer:
    def __init__(self):
        self.tables = ['articles','book','incollection','inproceedings','mastersthesis','phdthesis','proceedings']
        self.db = 'GAvI'
        self.host = 'localhost'
        self.user = 'niko'
        self.pw = 'nana'

        self.conn = ''

    def createColIndex(self):
        # Connessione con db
        print("Starting connection...")
        conn = psycopg2.connect(host=self.host, database=self.db, user=self.user, password=self.pw)
        cur = conn.cursor()
        print("Connection established.")

        for tab in self.tables:
            query = """
                    ALTER TABLE {0} ADD COLUMN ts_title tsvector;
                    ALTER TABLE {0} ADD COLUMN ts_authors tsvector;
                    ALTER TABLE {0} ADD COLUMN ts_year tsvector;
                    ALTER TABLE {0} ADD COLUMN ts_text_all tsvector;
                    ALTER TABLE {0} ADD COLUMN ts_venue_all tsvector;

                    UPDATE {0} SET ts_title = to_tsvector(title);
                    UPDATE {0} SET ts_authors = to_tsvector(authors);
                    UPDATE {0} SET ts_year = to_tsvector(year);
                    UPDATE {0} SET ts_text_all = to_tsvector(title || ' ' || authors || ' ' || year);
                    """.format(tab)

            query2 = ""
            if tab == 'articles':
                query2 = """
                        ALTER TABLE {0} ADD COLUMN ts_journal tsvector;
                        UPDATE {0} SET ts_journal = to_tsvector(journal);
                        UPDATE {0} SET ts_venue_all = to_tsvector(title || ' ' || journal);
                        """.format(tab)
            elif tab in ['proceedings','book','incollection']:
                query2 = """
                        ALTER TABLE {0} ADD COLUMN ts_publisher tsvector;
                        UPDATE {0} SET ts_publisher = to_tsvector(publisher);
                        UPDATE {0} SET ts_venue_all = to_tsvector(title || ' ' || publisher);
                        """.format(tab)

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
                query = """
                        CREATE INDEX {0}_idx ON {0}
                        USING GIN(ts_title,ts_authors,ts_year,ts_text_all);
                        """.format(tab)
            elif tab == 'articles':
                query = """
                        CREATE INDEX {0}_phrasal_idx ON {0}
                        USING GIN(ts_title,ts_authors,ts_year,ts_text_all);

                        CREATE INDEX {0}_venue_idx ON {0}
                        USING GIN(ts_journal,ts_venue_all);
                        """.format(tab)
            else:
                query = """
                        CREATE INDEX {0}_phrasal_idx ON {0}
                        USING GIN(ts_title,ts_authors,ts_year,ts_text_all);

                        CREATE INDEX {0}_venue_idx ON {0}
                        USING GIN(ts_publisher,ts_venue_all);
                        """.format(tab)

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
            query = """
                    DROP INDEX IF EXISTS {0}_idx;
                    DROP INDEX IF EXISTS {0}_phrasal_idx;
                    DROP INDEX IF EXISTS {0}_venue_idx;
                    """.format(tab)
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



if (sys.argv[1] == 'create'):
    ind = indexer()
    ind.createColIndex()
elif(sys.argv[1] == 'delete'):
    ind = indexer()
    ind.deleteIdx()

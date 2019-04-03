#!/usr/bin/python3
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os

import xml.sax
from saxParser import DBLPHandler

import sqlite3
from sqlite3 import Error

'''class index():
    def __init__(self):
        self.schema = Schema(title = TEXT(stored=TRUE),
                        author = TEXT(stored=TRUE),
                        year = NUMERIC(stored=TRUE)
                        publisher = TEXT
                        key = ID(stored = TRUE),
                        crossref = ID)

        if not os.path.exists('indice'):
            os.mkdir('indice')
        create_in('indice', schema)'''



def extractDataWithParser(path):
    print("Parsing {}...".format(path))
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    h = DBLPHandler()
    parser.setContentHandler(h)

    try:
        parser.parse(path)
    except FileNotFoundError:
        print("Errore! " + e)
        return False

    return h.data



'''Connessione con db, restituisce False se la connessione fallisce.'''
def connectToDb():
    try:
        conn = sqlite3.connect('../db/dbGAvI')
        return conn
    except Error as e:
        print(e)

    return False


def getData(dic, str):
    if dic.get(str):
        if str == 'author':
            app = ''
            for a in dic[str]:
                app+= a + ", "
            return app[:-2]
        else:
            return dic[str]
    else:
        return ''




'''inserimento di roba nel db.'''
def main():
    print("doing stuff...")

    data = extractDataWithParser("../dblp.xml")
    conn = connectToDb()
    c = conn.cursor()

    for dic in data:
        txt = "INSERT INTO article VALUES('{}','{}','{}',{},'{}','{}','{}','{}','{}')".format( \
                getData(dic,'key'), \
                getData(dic,'author'), \
                getData(dic,'title'), \
                getData(dic,'year'), \
                getData(dic,'url'), \
                getData(dic,'ee'), \
                getData(dic,'journal'), \
                getData(dic,'booktitle'), \
                getData(dic,'crossref'))
        try:
            c.execute(txt)
        except Error as e:
            print("Error! {} \n Query not executed: {}".format(e,txt))
            return

    conn.commit()
    conn.close()
    print('Done.')



if __name__ == '__main__':
    main()

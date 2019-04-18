#!/usr/bin/env python3

import sys
import psycopg2
import argparse


'''Classe per la ricerca nel db. In input vogliamo:
- La frase da cercare (viene trasformata in una tsquery).
- La tabella in cui lanciare la ricerca.
- Possibili argomenti extra.'''
class searchEng():
    def __init__(self,phrase,tab,**kwargs):
        self.phrase = phrase.replace(" "," | ") #potrebbe essere necessario sostituire '|' con '&'
        self.tab = tab
        self.year = kwargs['year']
        self.venue = kwargs['venue']
        self.ranking = kwargs['ranking']
        self.tables = ['articles','book','incollection','inproceedings','mastersthesis','phdthesis','proceedings','www']

        if self.year != None:
            self.phrase += ' & ' + str(kwargs['year']) #potrebbe essere necessario sostituire '&' con '|'



    '''
    Restituisce la query corretta a seconda dei parametri inseriti.
    (ci sono cose da sistemare)
    '''
    def __getQuery(self):
        # Query lanciata in caso in cui si debba prendere in consid. anche le proceedings
        if self.venue != None and self.tab in ['articles','inproceedings','incollections']:
            query = """
                        SELECT x.key, x.title, x.authors, x.year, x.url,
                        p.title,p.authors,p.year,p.editors,p.url,
                        ts_rank(x.ts_elements, xquery) + ts_rank(p.ts_elements,pquery) as ranking
                        FROM {} as x, proceedings as p, to_tsquery('{}') as xquery, to_tsquery('{}') as pquery
                        WHERE x.ts_elements @@ xquery
                        AND p.ts_elements @@ pquery
                        AND x.crossref = p.key;
                    """.format(self.tab,self.phrase,self.venue)

        elif self.venue != None:
            pass # da implementare
        else:
            # Query standard.
            query = """
                        SELECT x.*, ts_rank(x.ts_elements, query) as ranking
                        FROM {} as x, to_tsquery('{}') as query
                        WHERE x.ts_elements @@ query;
                    """.format(self.tab, self.phrase)
        return query



    '''Interrogazione del db.
    Restituisce il risultato (ordinato sulla base del ranking) della query,
    -1 se si verrifica un errore.'''
    def interrogation(self):
        print("Connessione con database...")
        conn = psycopg2.connect(host='localhost',
                                database='GAvI',
                                user='niko',
                                password='nana')
        cur = conn.cursor()

        try:
            if self.tab == 'publication':
                dic = {}
                for tab in self.tables:
                    self.tab = tab
                    print("Esecuzione query su ",self.tab)
                    query = self.__getQuery()
                    cur.execute(query)
                    ret = cur.fetchall()
                    # Ordinamento sulla base del ranking
                    dic[self.tab] = ret.sort(key = lambda x:x[-1], reverse = True)

                cur.close()
                conn.close()
                print("Esecuzione completata.")
                return dic

            elif self.tab in self.tables:
                print("Esecuzione query su ",self.tab)
                query = self.__getQuery()
                cur.execute(query)
                ret = cur.fetchall()
                cur.close()
                conn.close()
                print("Esecuzione completata.")

                # Ordinamento sulla base del ranking
                ret.sort(key = lambda x:x[-1], reverse = True)
                return ret

        except (Exception, psycopg2.Error) as e:
            print("An error occurred: ", e)
            cur.close()
            conn.close()
            return -1



'''
Lancio dello script.
Per funzionare correttamente, ecco come lanciare questo script:
        python3 search_engine.py 'stringa da ricercare' 'tabella' [parametri opzionali]
O anche solo:
        [PATH]/search_engine.py 'stringa da ricercare' 'tabella' [parametri opzionali]

Per ulteriori info digitare:    python3 search_engine.py -h
In questo caso argparse serve solo ed esclusivamente per gestire la correttezza dei parametri inseriti
'''
if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="search_engine", description ="Script per la ricerca di parole in un database di dati estratti da dblp.xml")

    parser.add_argument('frase', type=str, metavar='FRASE', help='Frase da ricercare nel db.')
    parser.add_argument('tabella', type=str, metavar='TABELLA', help='Tabella in cui effettuare la ricerca.')

    # Opzionali
    parser.add_argument("-y", "--year", type=int, metavar="YEAR",help="Inserimento dell'anno da ricercare.")
    parser.add_argument("-v", "--venue", type=str, metavar="VENUE", help="Parola specifica da ricercare oltre alla frase.")
    parser.add_argument("-r", "--ranking", type=str, metavar="RANKING", help="Specifico un determinato metodo di ranking.")
    #parser.add_argument("-f", "--fields", type=str, metavar="FIELDS", help='Specifico i campi su cui effettuare la ricerca.')

    # Recupero dei parametri.
    args = parser.parse_args()

    # Creazione search search_engine
    SE = search_engine(args.frase,
                        args.tabella,
                        year=args.year,
                        venue=args.venue,
                        ranking=args.ranking)

    # Esecuzione funzione di ricerca
    res = SE.interrogation()
    print(res)

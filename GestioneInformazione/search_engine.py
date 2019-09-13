#!/usr/bin/env python3

import argparse
import sys
from tkinter import messagebox

import psycopg2
# Algoritmo di ranking bm25
# In caso non sia installato eseguire 'pip3 install rank_bm25'
from rank_bm25 import BM25Okapi


class searchEng():
    def __init__(self,phrase,tab,**kwargs):
        self.phrase = phrase.replace(" "," | ")
        self.tab = tab
        self.year = kwargs['year']
        self.text_field = kwargs['text_field']
        self.venue = kwargs['venue']
        self.venue_field = kwargs['venue_field']
        self.ranking = kwargs['ranking']
        self.num = kwargs['num']
        self.tables = ['articles','book','incollection','inproceedings','mastersthesis','phdthesis','proceedings']

        if self.year != None and self.text_field == 'year':
            self.phrase = str(self.year).replace(" "," | ")
        elif self.year != None:
            self.phrase = '({}) & {}'.format(self.phrase, str(kwargs['year']))




    # Restituisce la query corretta a seconda dei parametri inseriti.
    # A seconda della tabella, che la venue sia inserita o no e del modello di ranking, la query è diversa.
    # L'ordinamento dei risultati in base al ranking viene gestito separatamente.
    def __getQuery(self):
        if self.venue != None and self.tab in ['inproceedings']:

            chance_x = "x.ts_text_all"
            chance_p = "p.ts_venue_all"

            if self.text_field != None:
                chance_x = "x.ts_{}".format(self.text_field)
            if self.venue_field != None:
                chance_p = "p.ts_{}".format(self.venue_field)


            rank = """, ts_rank({}, xquery) + ts_rank({},pquery) as ranking""".format(chance_x,chance_p)
            if self.ranking in ['bm25','BM25']:
                rank = ''

            query = """
                        SELECT x.key,x.title,x.authors,x.year,x.pages,x.url,
                        p.key,p.title,p.authors,p.year,p.publisher,p.url,
                        {3} as ts_x,
                        {4} as ts_p
                        {5}
                        FROM {0} as x,
                        proceedings as p,
                        to_tsquery('{1}') as xquery,
                        to_tsquery('{2}') as pquery
                        WHERE {3} @@ xquery
                        AND {4} @@ pquery
                        AND x.crossref = p.key;
                    """.format( self.tab,       #0
                                self.phrase,    #1
                                self.venue,     #2
                                chance_x,       #3
                                chance_p,       #4
                                rank            #5
                                )


        elif self.venue != None and self.tab in ['articles']:

            chance_x = "x.ts_text_all"
            chance_v = "x.ts_venue_all "

            if self.text_field != None:
                chance_x = "x.ts_{}".format(self.text_field)
            if self.venue_field != None:
                chance_v = "x.ts_{}".format(self.venue_field)

            rank = """, ts_rank({}, xquery) + ts_rank({},venue) as ranking""".format(chance_x,chance_v)
            if self.ranking in ['bm25','BM25']:
                rank = ''

            query = """
                        SELECT x.key,x.title,x.authors,x.year,x.journal,x.url,
                        {3} as ts_x,
                        {4} as ts_v
                        {5}
                        FROM {0} as x,
                        to_tsquery('{1}') as xquery,
                        to_tsquery('{2}') as venue
                        WHERE {3} @@ xquery
                        AND {4} @@ venue;
                    """.format( self.tab,       #0
                                self.phrase,    #1
                                self.venue,     #2
                                chance_x,       #3
                                chance_v,       #4
                                rank            #5
                                )


        elif self.venue != None and self.tab not in ['mastersthesis','phdthesis']:

            chance_x = "x.ts_text_all"
            chance_v = "x.ts_venue_all "

            if self.text_field != None:
                chance_x = "x.ts_{}".format(self.text_field)
            if self.venue_field != None:
                chance_v = "x.ts_{}".format(self.venue_field)

            url_or_ee = 'url'
            if self.tab in ['book','incollection']:
                url_or_ee ='ee'

            rank = """, ts_rank({}, query) + ts_rank({},venue) as ranking""".format(chance_x,chance_v)
            if self.ranking in ['bm25','BM25']:
                rank = ''

            query = """
                        SELECT x.key,x.title,x.authors,x.year,x.publisher,x.{5},
                        {3} as ts_x,
                        {4} as ts_v
                        {6}
                        FROM {0} as x,
                        to_tsquery('{1}') as query,
                        to_tsquery('{2}') as venue
                        WHERE {3} @@ query
                        AND {4} @@ venue;
                    """.format( self.tab,       #0
                                self.phrase,    #1
                                self.venue,     #2
                                chance_x,       #3
                                chance_v,       #4
                                url_or_ee,      #5
                                rank            #6
                                )


        else:
            chance_x = "x.ts_text_all"

            if self.text_field != None:
                chance_x = "x.ts_{}".format(self.text_field)

            url_or_ee = 'url'
            if self.tab in ['book','incollection']:
                url_or_ee ='ee'

            rank = """, ts_rank({}, query) as ranking""".format(chance_x)
            if self.ranking in ['bm25','BM25']:
                rank = ''

            # Creazione della query
            query = """
                SELECT x.key,x.title,x.authors,x.year,x.{3},
                {2} as ts_x
                {4}
                FROM {0} as x,
                to_tsquery('{1}') as query
                WHERE {2} @@ query;
                """.format( self.tab,       #0
                            self.phrase,    #1
                            chance_x,       #2
                            url_or_ee,      #3
                            rank            #4
                            )
        # Restituzione query
        print(query)
        return query





    def __bm25_ranking(self, lista):

        if self.ranking in ['bm25','BM25']:

            import nltk
            from nltk.corpus import stopwords
            wnl = nltk.WordNetLemmatizer()

            corpus_text = ''
            corpus_venue = ''

            if self.venue != None and self.tab in ['inproceedings']:
                corpus_text = [x['ts_i'] for x in lista]
                corpus_text = [x.replace("'", ' ').replace(":", ' ') for x in corpus_text]
                corpus_text = [nltk.word_tokenize(x) for x in corpus_text]
            else:
                corpus_text = [x['ts_tab'] for x in lista]
                corpus_text = [x.replace("'", ' ').replace(":", ' ') for x in corpus_text]
                corpus_text = [nltk.word_tokenize(x) for x in corpus_text]

            if self.venue != None and self.tab in ['inproceedings']:
                corpus_venue = [x['ts_p'] for x in lista]
                corpus_venue = [x.replace("'", ' ').replace(":", ' ') for x in corpus_venue]
                corpus_venue = [nltk.word_tokenize(x) for x in corpus_venue]

            elif self.venue != None:
                corpus_venue = [x['ts_venue'] for x in lista]
                corpus_venue = [x.replace("'", ' ').replace(":", ' ') for x in corpus_venue]
                corpus_venue = [nltk.word_tokenize(x) for x in corpus_venue]


            bm25_text = BM25Okapi(corpus_text)

            bm25_venue = ''
            if self.venue != None:
                bm25_venue = BM25Okapi(corpus_venue)

            query = nltk.word_tokenize(self.phrase)
            tokens = [wnl.lemmatize(x) for x in query if x not in stopwords.words('english') ]

            text_ranks = list(bm25_text.get_scores(tokens))

            venue_ranks = ''
            if bm25_venue != '':
                venue = nltk.word_tokenize(self.venue)
                tokens_venue = [wnl.lemmatize(x) for x in venue if x not in stopwords.words('english') ]
                venue_ranks = list(bm25_venue.get_scores(tokens_venue))

                text_ranks = [text_ranks[cont] + venue_ranks[cont] for cont in range(len(text_ranks))]

            new_lista = []
            c = 0
            for x in lista:
                x['ranking'] = text_ranks[c]
                new_lista.append(x)
                c+=1

            return new_lista
        else:
            return lista






    def __getDictResults(self,results):
        lista = []
        diz = {}

        if self.venue != None and self.tab in ['inproceedings']:
            keys = ['i_key','i_title','i_authors','i_year','i_pages','i_url',
            'p_key','p_title','p_authors','p_year','p_publisher','p_url','ts_i','ts_p']

            if self.ranking not in ['bm25', 'BM25']:
                keys.append('ranking')

            for elem in results:
                diz = {keys[cont]:elem[cont] for cont in range(len(keys)) if elem[cont]!=''}
                lista.append(diz)
            return lista



        elif self.venue != None and self.tab in ['articles']:
            keys = ['key','title','authors','year','journal','url','ts_tab','ts_venue']

            if self.ranking not in ['bm25', 'BM25']:
                keys.append('ranking')

            for elem in results:
                diz = {keys[cont]:elem[cont] for cont in range(len(keys)) if elem[cont]!=''}
                lista.append(diz)
            return lista



        elif self.venue != None and self.tab not in ['mastersthesis','phdthesis']:

            url_or_ee = 'url'
            if self.tab in ['book','incollection']:
                url_or_ee ='ee'

            keys = ['key','title','authors','year','publisher',url_or_ee,'ts_tab','ts_venue']

            if self.ranking not in ['bm25', 'BM25']:
                keys.append('ranking')

            for elem in results:
                diz = {keys[cont]:elem[cont] for cont in range(len(keys)) if elem[cont]!=''}
                lista.append(diz)
            return lista



        else:
            url_or_ee = 'url'
            if self.tab in ['book','incollection']:
                url_or_ee ='ee'

            keys = ['key','title','authors','year',url_or_ee,'ts_tab']

            if self.ranking not in ['bm25', 'BM25']:
                keys.append('ranking')

            for elem in results:
                diz = {keys[cont]:elem[cont] for cont in range(len(keys)) if elem[cont]!=''}
                lista.append(diz)
            return lista






    def interrogation(self):
        try:
            conn = psycopg2.connect(host='localhost',
                                    database='GAvI',
                                    user='niko',
                                    password='nana')
            cur = conn.cursor()
        except Exception:
            messagebox.showerror(title="Error", message="Is the server running on host \"localhost\" (127.0.0.1) and "
                                                        "accepting TCP/IP connections on port 5432?")
            return

        try:
            if self.tab == 'publication':
                dic = {}

                for tab in self.tables:

                    self.tab = tab
                    query = self.__getQuery()
                    cur.execute(query)
                    ret = cur.fetchall()

                    pre_ranking = self.__getDictResults(ret)

                    dic[self.tab] = self.__bm25_ranking(pre_ranking)

                    dic[self.tab].sort(key = lambda x:x['ranking'], reverse = True)

                    if self.num != None and self.num < len(dic):
                        dic[self.tab] = dic[self.tab][0:self.num]


                cur.close()
                conn.close()
                return dic

            elif self.tab in self.tables:
                query = self.__getQuery()
                cur.execute(query)
                ret = cur.fetchall()
                cur.close()
                conn.close()

                pre_ranking = self.__getDictResults(ret)

                dic = self.__bm25_ranking(pre_ranking)

                dic.sort(key = lambda x:x['ranking'], reverse = True)

                if self.num != None and self.num < len(dic):
                    dic = dic[0:self.num]

                return dic

        except (Exception, psycopg2.Error) as e:
            print("An error occurred: ", e)
            cur.close()
            conn.close()
            return -1




if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="search_engine", description ="Script per la ricerca di parole in un database di dati estratti da dblp.xml")

    parser.add_argument('frase', type=str, metavar='FRASE', help='Frase da ricercare nel db.')
    parser.add_argument('tabella', type=str, metavar='TABELLA', help='Tabella in cui effettuare la ricerca.')

    # Opzionali
    parser.add_argument("-y", "--year", type=int, metavar="YEAR",help="Inserimento dell'anno da ricercare.")
    parser.add_argument("-tf", "--text_field", type=str, metavar="TEXT_FIELD", choices=['authors','year','title'],help="Inserimento del campo in cui fare la full text search (author | title | year). Se vuoto, cerco in tutti e tre.")
    parser.add_argument("-v", "--venue", type=str, metavar="VENUE", help="Parola specifica da ricercare oltre alla frase.")
    parser.add_argument("-tv", "--venue_field", type=str, metavar="VENUE_FIELD", choices=['title','publisher','journal'],help="Inserimento del campo in cui cercare la venue (title | publisher | journal, journal si può scegliere solo se la tabella in cui cercare è article). Se vuoto, cerco in tutti.")
    parser.add_argument("-r", "--ranking", type=str, metavar="RANKING", choices=['boolean','bm25','BM25'], help="Specifico un determinato metodo di ranking.")
    parser.add_argument("-n", "--num", type=int, metavar="NUM", help='Specifico il numero di risultati da visualizzare.')

    # Recupero dei parametri.
    args = parser.parse_args()

    # Creazione search search_engine
    SE = searchEng(args.frase,
                        args.tabella,
                        year=args.year,
                        text_field=args.text_field,
                        venue=args.venue,
                        venue_field=args.venue_field,
                        ranking=args.ranking,
                        num=args.num)

    # Esecuzione funzione di ricerca
    res = SE.interrogation()

    # Restituzione roba (non so se così è il modo giusto)
    sys.exit(res)

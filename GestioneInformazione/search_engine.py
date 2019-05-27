#!/usr/bin/env python3

import sys
import psycopg2
import argparse

# Algoritmo di ranking bm25
# In caso non sia instalalto eseguire 'pip3 install rank_bm25'
from rank_bm25 import BM25Okapi


# Classe per la ricerca nel db. In input vogliamo:
# La frase da cercare: 'phrase' (viene trasformata in una tsquery).
# (Le ricerche sono fatte in OR)
# La tabella in cui lanciare la ricerca: 'tab'.
# Possibili argomenti extra in 'kwargs':
#   - n: Numero di elementi recuperati che vogliamo visualizzare.
#        (se 'n' è superiore del numero di elem. recuperati, allora si ignora 'n')
#   - venue: Venue di ricerca, non deve essere specificato obbligatoriamente.
#   - text_field: campo in cui fare full-text-search della frase 'phrase'
#                 (possibili opzioni: 'title', 'authors' OPPURE 'year'.
#                 In caso sia lasciato vuoto, si ricerca in tutti e 3 i campi.)
#   - venue_field: campo in cui fare full-text-search della venue, se specificata.
#                 (possibili opzioni: 'title' OR 'journal', se la tabella di ricerca è 'articles',
#                  oppure 'title' OR 'publisher' in tutti gli altri casi. Se la tabella è 'inproceedings'
#                  la venue va cercata nel 'proceedings' ad esso associato.
#                 In caso sia lasciato vuoto, si ricerca in tutte 2 i campi.)
#   - ranking: permette di specificare il modello di ranking da utilizzare (possibili opzioni: boolean e bm25).
#   - year: permette di specificare l'anno da ricercare.
class searchEng():
    def __init__(self,phrase,tab,**kwargs):
        self.phrase = phrase.replace(" "," | ") #potrebbe essere necessario sostituire '|' con '&'
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
            self.phrase += ' | ' + str(kwargs['year']) #potrebbe essere necessario sostituire '|' con '&'




    # Restituisce la query corretta a seconda dei parametri inseriti.
    # A seconda della tabella, che la venue sia inserita o no e del modello di ranking, la query è diversa.
    # L'ordinamento dei risultati in base al ranking viene gestito separatamente.
    def __getQuery(self):
        # Query lanciata in caso in cui la tabella sia INPROCEEDINGS e sia stata inserita la VENUE
        if self.venue != None and self.tab in ['inproceedings']:

            # Query-injection dei campi su cui fare full-text-search di 'phrase' e 'venue'
            chance_x = "x.ts_title||' '||x.ts_authors||' '||x.ts_year"
            chance_p = "p.ts_title||' '||p.ts_publisher"

            # Casi in cui text_field e venue_field siano stati inseriti
            if self.text_field != None:
                chance_x = "x.ts_{}".format(self.text_field)
            if self.venue_field != None:
                chance_p = "p.ts_{}".format(self.venue_field)

            # Gestione del ranking:
            #  - se il modello è 'boolean', allora il ranking viene gestito direttamente nella query
            #  - altrimenti (modello bm25) il ranking sarà gestito esternamente.
            rank = """, ts_rank({}, xquery) + ts_rank({},pquery) as ranking""".format(chance_x,chance_p)
            if self.ranking in ['bm25','BM25']:
                rank = ''

            # Creazione della query
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


        # Query lanciata in caso in cui la tabella sia ARTICLES e sia stata inserita la VENUE
        elif self.venue != None and self.tab in ['articles']:

            # Query-injection dei campi su cui fare full-text-search di 'phrase' e 'venue'
            chance_x = "x.ts_title||' '||x.ts_authors||' '||x.ts_year"
            chance_v = "x.ts_title||' '||x.ts_journal "

            # Casi in cui text_field e venue_field siano stati inseriti
            if self.text_field != None:
                chance_x = "x.ts_{}".format(self.text_field)
            if self.venue_field != None:
                chance_v = "x.ts_{}".format(self.venue_field)

            # Gestione del ranking:
            #  - se il modello è 'boolean', allora il ranking viene gestito direttamente nella query
            #  - altrimenti (modello bm25) il ranking sarà gestito esternamente.
            rank = """, ts_rank({}, xquery) + ts_rank({},venue) as ranking""".format(chance_x,chance_v)
            if self.ranking in ['bm25','BM25']:
                rank = ''

            # Creazione della query
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


        # Query lanciata in caso in cui la tabella NON sia MASTERSTHESIS o PHDTHESIS (che non hanno il campo publisher)
        # e sia stata inserita la VENUE
        elif self.venue != None and self.tab not in ['mastersthesis','phdthesis']:

            # Query-injection dei campi su cui fare full-text-search di 'phrase' e 'venue'
            chance_x = "x.ts_title||' '||x.ts_authors||' '||x.ts_year "
            chance_v = "x.ts_title||' '||x.ts_publisher"

            # Casi in cui text_field e venue_field siano stati inseriti
            if self.text_field != None:
                chance_x = "x.ts_{}".format(self.text_field)
            if self.venue_field != None:
                chance_v = "x.ts_{}".format(self.venue_field)

            # In 'book' e 'incollection', il campo url non è presente.
            # In questi casi, si restituisce il campo ee, al posto di url.
            url_or_ee = 'url'
            if self.tab in ['book','incollection']:
                url_or_ee ='ee'

            # Gestione del ranking:
            #  - se il modello è 'boolean', allora il ranking viene gestito direttamente nella query
            #  - altrimenti (modello bm25) il ranking sarà gestito esternamente.
            rank = """, ts_rank({}, query) + ts_rank({},venue) as ranking""".format(chance_x,chance_v)
            if self.ranking in ['bm25','BM25']:
                rank = ''

            # Creazione della query
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


        # Query standard, senza VENUE
        else:
            # Query-injection dei campi su cui fare full-text-search di 'phrase'
            chance_x = "x.ts_title||' '||x.ts_authors||' '||x.ts_year"

            # Caso in cui il text_field sia stato inserito
            if self.text_field != None:
                chance_x = "x.ts_{}".format(self.text_field)

            # In 'book' e 'incollection', il campo url non è presente.
            # In questi casi, si restituisce il campo ee, al posto di url.
            url_or_ee = 'url'
            if self.tab in ['book','incollection']:
                url_or_ee ='ee'

            # Gestione del ranking:
            #  - se il modello è 'boolean', allora il ranking viene gestito direttamente nella query
            #  - altrimenti (modello bm25) il ranking sarà gestito esternamente.
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





    # Gestione del ranking bm25Okapi. Purtroppo è stato fatto separatamente.
    # I modelli implementati sono quello booleano e il BM25Okapi. In caso l'utente non specifici il modello,
    # di default viene utilizzato quello booleano. Questa funzione gestisce il BM25, che:
    #   - Prende in input i risultati della query (lista di dizionari) e ne calcola il peso.
    #   - Restituisce la lista di diz. dove ogni elemento è pesato.
    # Se non è stato scelto il modello bm25, non succede nulla.
    # Se è stata inserita anche la ricerca della venue, si considera anche il suo ranking
    def __bm25_ranking(self, lista):

        #Se non è stato scelto il bm25, non succede nulla.
        if self.ranking in ['bm25','BM25']:

            #Creazione oggetti per il preprocessing
            import nltk
            from nltk.corpus import stopwords
            wnl = nltk.WordNetLemmatizer()

            # Campi necessari per inizializzare la ricerca del bm25
            corpus_text = ''
            corpus_venue = ''

            # 'Normalizzazione' del testo di ricerca della 'phrase' da 'indicizzare' per il ranking
            if self.venue != None and self.tab in ['inproceedings']:
                corpus_text = [x['ts_i'] for x in lista]
                corpus_text = [x.replace("'", ' ').replace(":", ' ') for x in corpus_text]
                corpus_text = [nltk.word_tokenize(x) for x in corpus_text]
            else:
                corpus_text = [x['ts_tab'] for x in lista]
                corpus_text = [x.replace("'", ' ').replace(":", ' ') for x in corpus_text]
                corpus_text = [nltk.word_tokenize(x) for x in corpus_text]

            # 'Normalizzazione' delle venue da 'indicizzare' per il ranking
            if self.venue != None and self.tab in ['inproceedings']:
                corpus_venue = [x['ts_p'] for x in lista]
                corpus_venue = [x.replace("'", ' ').replace(":", ' ') for x in corpus_venue]
                corpus_venue = [nltk.word_tokenize(x) for x in corpus_venue]

            elif self.venue != None:
                corpus_venue = [x['ts_venue'] for x in lista]
                corpus_venue = [x.replace("'", ' ').replace(":", ' ') for x in corpus_venue]
                corpus_venue = [nltk.word_tokenize(x) for x in corpus_venue]


            # Indicizzazione tramite bm25 sul testo
            bm25_text = BM25Okapi(corpus_text)

            # Indicizzazione tramite bm25 sulla venue (se presente)
            bm25_venue = ''
            if self.venue != None:
                bm25_venue = BM25Okapi(corpus_venue)

            # Preprocessing della 'phrase' da analizzare
            query = nltk.word_tokenize(self.phrase)
            tokens = [wnl.lemmatize(x) for x in query if x not in stopwords.words('english') ]

            # Recupero dei pesi per ogni documento (relativamente alla full-text-search della frase)
            text_ranks = list(bm25_text.get_scores(tokens))

            # Se la venue è stata inserita, aggiungo il suo peso al peso ottenuto facendo il ranking del testo
            venue_ranks = ''
            if bm25_venue != '':
                venue = nltk.word_tokenize(self.venue)
                tokens_venue = [wnl.lemmatize(x) for x in venue if x not in stopwords.words('english') ]
                venue_ranks = list(bm25_venue.get_scores(tokens_venue))

                # Aggiunta dei pesi della venue a quelli della frase
                text_ranks = [text_ranks[cont] + venue_ranks[cont] for cont in range(len(text_ranks))]

            # AGGIORNAMENTO DELLA LISTA, INSERIMENTO DEI RANKING
            new_lista = []
            c = 0
            for x in lista:
                x['ranking'] = text_ranks[c]
                new_lista.append(x)
                c+=1

            # Restituzione nuova lista
            return new_lista
        # Caso in cui sia stato scelto il modello booleano di ranking
        else:
            return lista






    # Dati i risultati (sotto forma di lista), restituisce l'equivalente sotto forma di lista di dizionari.
    # Facilita il successivo accesso ai risultati.
    def __getDictResults(self,results):
        lista = []
        diz = {}

        #Caso in cui la tabella in cui ricercare sia INPROCEEDINGS e sia inserita la VENUE
        if self.venue != None and self.tab in ['inproceedings']:
            #Specifico le chiavi (NON MODIFICARE L'ORDINE)
            keys = ['i_key','i_title','i_authors','i_year','i_pages','i_url',
            'p_key','p_title','p_authors','p_year','p_publisher','p_url','ts_i','ts_p']

            # Gestione del ranking: se il modello booleano è scelto, sarà gestito nelle query e quindi sarà
            # necessario considerare una chiave apposta per il campo ranking. Altrimenti, il ranking sarà
            # inserito successivamente.
            if self.ranking not in ['bm25', 'BM25']:
                keys.append('ranking')

            # Creazione di una lista di dizionari per ogni documento recuperato, con le chiavi precedentemente specificate.
            for elem in results:
                diz = {keys[cont]:elem[cont] for cont in range(len(keys)) if elem[cont]!=''}
                lista.append(diz)
            return lista



        #Caso in cui la tabella in cui ricercare sia ARTICLES e sia inserita la VENUE
        elif self.venue != None and self.tab in ['articles']:
            #Specifico le chiavi (NON MODIFICARE L'ORDINE)
            keys = ['key','title','authors','year','journal','url','ts_tab','ts_venue']

            # Gestione del ranking: se il modello booleano è scelto, sarà gestito nelle query e quindi sarà
            # necessario considerare una chiave apposta per il campo ranking. Altrimenti, il ranking sarà
            # inserito successivamente.
            if self.ranking not in ['bm25', 'BM25']:
                keys.append('ranking')

            # Creazione di una lista di dizionari per ogni documento recuperato, con le chiavi precedentemente specificate.
            for elem in results:
                diz = {keys[cont]:elem[cont] for cont in range(len(keys)) if elem[cont]!=''}
                lista.append(diz)
            return lista



        # Caso in cui la tabella in cui ricercare NON sia MASTERSTHESIS e PHDTHESIS e sia inserita la VENUE
        elif self.venue != None and self.tab not in ['mastersthesis','phdthesis']:

            # In 'book' e 'incollection', il campo url non è presente.
            # In questi casi, si restituisce il campo ee, al posto di url.
            url_or_ee = 'url'
            if self.tab in ['book','incollection']:
                url_or_ee ='ee'

            #Specifico le chiavi (NON MODIFICARE L'ORDINE)
            keys = ['key','title','authors','year','publisher',url_or_ee,'ts_tab','ts_venue']

            # Gestione del ranking: se il modello booleano è scelto, sarà gestito nelle query e quindi sarà
            # necessario considerare una chiave apposta per il campo ranking. Altrimenti, il ranking sarà
            # inserito successivamente.
            if self.ranking not in ['bm25', 'BM25']:
                keys.append('ranking')

            # Creazione di una lista di dizionari per ogni documento recuperato, con le chiavi precedentemente specificate.
            for elem in results:
                diz = {keys[cont]:elem[cont] for cont in range(len(keys)) if elem[cont]!=''}
                lista.append(diz)
            return lista



        # Caso standard, senza la VENUE
        else:
            # In 'book' e 'incollection', il campo url non è presente.
            # In questi casi, si restituisce il campo ee, al posto di url.
            url_or_ee = 'url'
            if self.tab in ['book','incollection']:
                url_or_ee ='ee'

            #Specifico le chiavi (NON MODIFICARE L'ORDINE)
            keys = ['key','title','authors','year',url_or_ee,'ts_tab']

            # Gestione del ranking: se il modello booleano è scelto, sarà gestito nelle query e quindi sarà
            # necessario considerare una chiave apposta per il campo ranking. Altrimenti, il ranking sarà
            # inserito successivamente.
            if self.ranking not in ['bm25', 'BM25']:
                keys.append('ranking')

            # Creazione di una lista di dizionari per ogni documento recuperato, con le chiavi precedentemente specificate.
            for elem in results:
                diz = {keys[cont]:elem[cont] for cont in range(len(keys)) if elem[cont]!=''}
                lista.append(diz)
            return lista






    # Interrogazione del db.
    # Nel caso la tabella in cui si deve ricercare sia 'publication', la ricerca viene effettuata su tutte le
    # altre yabelle.
    # Restituisce il risultato (ordinato sulla base del ranking) della query,
    # -1 se si verrifica un errore.
    def interrogation(self):
        # Connessione con il db
        print("Connessione con database...")
        conn = psycopg2.connect(host='localhost',
                                database='GAvI',
                                user='niko',
                                password='nana')
        cur = conn.cursor()

        try:
            # Caso in cui ricercare in tutte le tabelle
            if self.tab == 'publication':
                dic = {}

                for tab in self.tables:

                    # Recupero dei risultati
                    self.tab = tab
                    print("Esecuzione query su ",self.tab)
                    query = self.__getQuery()
                    cur.execute(query)
                    ret = cur.fetchall()

                    # Trasformazione dei risultati in dizionario
                    pre_ranking = self.__getDictResults(ret)

                    # Inserimento del ranking con bm25
                    dic[self.tab] = self.__bm25_ranking(pre_ranking)

                    #Ordinamento sulla base del ranking
                    dic[self.tab].sort(key = lambda x:x['ranking'], reverse = True)

                    # Restituzione dei primi n elementi (se N è specificato)
                    if self.num != None and self.num < len(dic):
                        dic[self.tab] = dic[self.tab][0:self.num]


                cur.close()
                conn.close()
                print("Esecuzione completata.")
                return dic

            # Caso in cui ricercare in una sola tabella
            elif self.tab in self.tables:
                print("Esecuzione query su ",self.tab)
                query = self.__getQuery()
                cur.execute(query)
                ret = cur.fetchall()
                cur.close()
                conn.close()
                print("Esecuzione completata.")

                # Trasformazione della lista in dizionario
                pre_ranking = self.__getDictResults(ret)

                # Inserimento dei pesi dei documenti
                dic = self.__bm25_ranking(pre_ranking)

                #Ordinamento sulla base del RANKING
                dic.sort(key = lambda x:x['ranking'], reverse = True)

                # Restituzione dei primi n elementi (se N è specificato)
                if self.num != None and self.num < len(dic):
                    dic = dic[0:self.num]

                return dic

        except (Exception, psycopg2.Error) as e:
            print("An error occurred: ", e)
            cur.close()
            conn.close()
            return -1




# Lancio del search engine tramite script.
# Per funzionare correttamente, ecco come lanciare questo script:
#         python3 search_engine.py 'stringa da ricercare' 'tabella' [parametri opzionali]
# O anche solo:
#         [PATH]/search_engine.py 'stringa da ricercare' 'tabella' [parametri opzionali]
#
# Per ulteriori info sui parametri opzionali, ecc, digitare:    python3 search_engine.py -h
# In questo caso argparse serve solo ed esclusivamente per gestire la correttezza dei parametri inseriti
# Si presuppone che la correttezza dei parametri sia verificata dall'interfaccia grafica
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

# GestioneInformazione

Progetto per il mitico esame di Gestione dell'Informazione Avanzata(è la prima volta che uso GitHub per qualcosa che non sia scaricare puttanate). ENJOY.

---

###What has been done:

Parser funzionante: estrae i dati e li infila nel database GAvI di postgresql.
Affinchè il parser funzioni è necessario *inserire dblp.xml* nella stessa cartella in è inserito *parser.py*.
---
Prima di importare il database da *db.gz* assicurarsi di:
	- Avere postgresql.
	- Estrarre l'archivio compresso db.gz con `gunzip -c db.gz | psql GAvI`.
	- Su *postgresql* (da linea di comando eseguire `su - postgres psql`) creare l'user *niko* con password *nana* by typing `create user niko with password 'nana';`.
	- Quindi eseguire `grant all privileges on database GAvI to niko;`.
In questo modo dovreste riuscire a importare il db con tutti i dati. Se preferite usare pgAdmin per fare questi passaggi, feel free to do that my dudes.

*indexing.py* contiene la classe che crea l'indice su tutte le tabelle del database.
	 

# GestioneInformazione
Python graphical interface to query dblp data.
## Getting Started
How to properly download and install `GestioneInformazione`.
### Prerequisites
Few things are required.
* Python3

* PostgreSQL

Login:
```
$ su - postgres psql
```
Or
```
$ sudo -u postgres psql postgres
```
Create user `niko` with password `nana`:
```
# create user niko with password 'nana';
```
Create DB:
```
# CREATE DATABASE GAvI;
```
And grant all privileges to that user:
```
# grant all privileges on database GAvI to niko;
```

* dblp.xml file

Download from [here](https://dblp.uni-trier.de/xml/) and move into GestioneInformazione/GestioneInformazione/dblp.xml
* psycopg2 and rank_bm25
```
$ pip3 install [psycopg2 | rank_bm25 | nltk]
```
* `GestioneInformazione` package
```
$ git clone https://github.com/niko0097/GestioneInformazione
```
Or just hit the [link](https://github.com/niko0097/GestioneInformazione) and click download.
### Installing
Just go into the directory `GestioneInformazione` and run the following instructions.

Setup package:
```
$ python3 setup.py sdist
```
And install..
```
$ python3 setup.py install
```
Populate DB:
```
$ python3 GestioneInformazione/parser.py
```
Create the indexes:
```
$ python3 GestioneInformazione/indexing.py
```
## Running

Now you are able to run our package, `supersearch` bash command is part of your system.
## Authors
**Cristian Gabbi** see GitHub [page](https://github.com/cristiangabbi)

**Nicola Baccarani** see GitHub [page](https://github.com/niko0097)

**Giorgio Martino** see GitHub [page](https://github.com/GiorgioMartino)

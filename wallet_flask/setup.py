import logging
import sqlite3

database = 'db.sqlite3'

queries = []

query = '''CREATE TABLE "master" (
	"coin"	TEXT NOT NULL UNIQUE,
	"seed"	TEXT NOT NULL,
	"private_key"	TEXT NOT NULL,
	"chain_code"	TEXT NOT NULL,
	PRIMARY KEY("coin")
    );'''

queries.append(query)

query = '''CREATE TABLE "address" (
	"id"	INTEGER NOT NULL UNIQUE,
	"coin"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
    );'''

queries.append(query)

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('main start')
    con = sqlite3.connect(database)
    cur = con.cursor()
    for query in queries:
        logging.debug(f'executing {query}')
        cur.execute(query)
        con.commit()
    con.close()
    logging.debug('main ended')


if __name__ == '__main__':
    main()


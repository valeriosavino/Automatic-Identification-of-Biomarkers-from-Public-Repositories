import psycopg2

def createDB():
    #creazione connessione al database di default di PostgreSQL "postgres"
    conn = psycopg2.connect(database="postgres", user="postgres", password="root", host="127.0.0.1", port= "5432")

    conn.autocommit = True

    #esecutore di statements
    cur = conn.cursor()

    cur.execute('''SELECT datname FROM pg_catalog.pg_database WHERE datname = \'hpatlas\'''')

    if(len(rs)==0):
        cur.execute('''CREATE DATABASE hpatlas''')
        print('Database creato con successo')

    #chiusura cur
    cur.close()

    #Closing the connection
    conn.close()
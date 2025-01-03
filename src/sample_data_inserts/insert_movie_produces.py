import os
import random
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv


def makeSQLStatement():
    statements = []
    for i in range(0,999):
        r = random.randint(0, 174)
        statements.append((i, r))
    return statements

def sshTunnel():
    try:
        load_dotenv()
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        dbName = "p320_11"

        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('127.0.0.1', 5432)) as server:
            server.start()
            print("SSH tunnel established")

            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }
            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            print("Database connection established")

            insert_query = """
                INSERT INTO movieproduces (movieid, studioid) VALUES (%s, %s)
                """
            statements = makeSQLStatement()
            curs.executemany(insert_query, statements)
            conn.commit()
            print("All movie-producer relations inserted successfully!")
            conn.close()


    except:
        print("Connection failed")



def main():
    makeSQLStatement()
    sshTunnel()



if __name__ == "__main__":
    main()
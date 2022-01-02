import psycopg2
from psycopg2 import Error
try:
    
    connection = psycopg2.connect(
                            database='diplomadb',
                            user='diploma',
                            password='diploma',
                            host='localhost',
                            port='5432'
                            )
    cursor = connection.cursor()

    create_table_query = '''CREATE TABLE music
                            (ID INT PRIMARY KEY NOT NULL,
                            KIND TEXT NOT NULL,
                            COLLECTIONNAME TEXT NOT NULL,
                            TRACKNAME TEXT NOT NULL,
                            COLLECTIONPRICE REAL NOT NULL,
                            TRACKPRICE REAL NOT NULL,
                            PRIMARYGENRENAME TEXT NOT NULL,
                            TRACKCOUNT INT NOT NULL,
                            RELEASEDATE TEXT NOT NULL);'''

    cursor.execute(create_table_query)
    
    #cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc,def"))
    connection.commit()
    print("Table created")
except (Exception, Error) as error:
    print("Failure", error)
finally:
    cursor.close()
    connection.close()

    #cur.execute("SELECT * FROM my_data")
    #records = cur.fetchall()

##  CREATE DB

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

    create_table_query = '''CREATE TABLE IF NOT EXISTS music
                            (ID SERIAL PRIMARY KEY,
                            KIND TEXT,
                            COLLECTIONNAME TEXT,
                            TRACKNAME TEXT,
                            COLLECTIONPRICE REAL,
                            TRACKPRICE REAL,
                            PRIMARYGENRENAME TEXT,
                            TRACKCOUNT INT,
                            TRACKNUMBER INT,
                            RELEASEDATE TEXT);'''

    cursor.execute(create_table_query)
    
    
    connection.commit()
    print("Table created")
except (Exception, Error) as error:
    print("Failure", error)
finally:
    cursor.close()
    connection.close()
   
## DO REQUEST

# import modules
import requests
import json

#Do search request with band name
band = 'beatles'
limit = 1
itunes_search_link = f'https://itunes.apple.com/search?term={band}&limit={limit}&entity=allArtist&attribute=allArtistTerm'
response = requests.get(itunes_search_link)

# Get artistid from json respond
temp0 = json.loads(response.content)
temp1 = temp0.get('results')
temp2 = temp1[0]
artist_id = temp2['artistId']
print(artist_id)

# Do lookup request using artistid

#artist_id = 136975

limit = 50
itunes_lookup_link = f'https://itunes.apple.com/lookup?id={artist_id}&entity=song&limit={limit}'

response = requests.get(itunes_lookup_link)

temp0 = json.loads(response.content)
temp1 = temp0.get('results')
temp2 = temp1[1:] #temp is full list
songs = [] #songs is needed list

#Filter dict to get only requested keys
for temp in temp2:
    newmusic = {}
    newmusic['kind'] = temp.get('kind', "No Value")
    newmusic['collectionName'] = temp.get('collectionName', "No Value")
    newmusic['trackName'] = temp.get('trackName', "No Value")
    newmusic['collectionPrice'] = temp.get('collectionPrice', "No Value")
    newmusic['trackPrice'] = temp.get('trackPrice', "No Value")
    newmusic['primaryGenreName'] = temp.get('primaryGenreName', "No Value")
    newmusic['trackCount'] = temp.get('trackCount', "No Value")
    newmusic['trackNumber'] = temp.get('trackNumber', "No Value")
    newmusic['releaseDate'] = temp.get('releaseDate', "No Value")

    songs.append(newmusic)

## FILL DB

for song in songs:
    insert_table_query = '''INSERT INTO music(KIND,
                            COLLECTIONNAME,
                            TRACKNAME,
                            COLLECTIONPRICE,
                            TRACKPRICE,
                            PRIMARYGENRENAME,
                            TRACKCOUNT,
                            TRACKNUMBER,
                            RELEASEDATE)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    connection = psycopg2.connect(
                                database='diplomadb',
                                user='diploma',
                                password='diploma',
                                host='localhost',
                                port='5432'
                                    )
    cursor = connection.cursor()
    cursor.execute(insert_table_query, list(song.values()))
    
    connection.commit()
    cursor.close()
    connection.close()



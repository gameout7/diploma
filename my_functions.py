##  CREATE DB

import psycopg2
from psycopg2 import Error
from requests.api import get

def create_table():
    """
    Creates table in Postgres DB
    """
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

def get_artist_id(band):
    """
    get artist id using search request to itunes API
    need requests, json
    """

    #Do search request with band name
    limit = 1
    itunes_search_link = f'https://itunes.apple.com/search?term={band}&limit={limit}&entity=allArtist&attribute=allArtistTerm'
    response = requests.get(itunes_search_link)

    # Get artistid from json respond
    temp0 = json.loads(response.content)
    temp1 = temp0.get('results')
    temp2 = temp1[0]
    artist_id = temp2['artistId']
    return artist_id
#    print(artist_id)

    # Do lookup request using artistid

artist_id = get_artist_id("beatles")
print(artist_id)

def get_atist_songs(artist_id, limit='10'):
    """
    Returns list of song request artist id using lookup request itunes API
    need requests, json
    """
    #limit = 50
    # Do lookup request using artistid
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
    
    return songs

songs = get_atist_songs(artist_id, 10)
print(songs[0])
## FILL DB

def fill_table(songs):
    """
    Fill database table with songs
    """
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



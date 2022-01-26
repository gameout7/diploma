##  CREATE DB

from fileinput import filename
import psycopg2
from psycopg2 import Error, connect, extras

from requests.api import get
from configparser import ConfigParser

def config(filename='database.ini', section='db'):
    """Get connection details from file"""
    parser = ConfigParser()
    parser.read(filename)
    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not fount in {filename}')
    return db


def create_table():
    """
    Creates table in Postgres DB
    """
    connection = None

    try:
        
        params = config()
        connection = psycopg2.connect(**params)
 
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
#        print("Table created")
    except (Exception, Error) as error:
        print("Failure", error)
    finally:
        cursor.close()
        connection.close()
   
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

def get_artist_songs(artist_id, limit='10'):
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

def get_artist_songs2(artist_id, limit='10'):
    """
    Returns list of all songs request artist id using lookup request itunes API
    need requests, json
    """
    #limit = 50
    # Do lookup request using artistid
    songs = [] #songs is needed list
    offset = 0
    while True:
        itunes_lookup_link = f'https://itunes.apple.com/lookup?id={artist_id}&entity=song&limit={limit}&offset={offset}'

        response = requests.get(itunes_lookup_link)

        temp0 = json.loads(response.content)
        temp1 = temp0.get('results')
        temp2 = temp1[1:] #temp is full list
 #       songs = [] #songs is needed list
        
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
        offset += 200
        print(len(songs))
        if len(songs) < limit:
            break
    return songs

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

        connection = None

        try:
            
            params = config()
            connection = psycopg2.connect(**params)
    
            cursor = connection.cursor()

            cursor.execute(insert_table_query, list(song.values()))
                    
            connection.commit()

        except (Exception, Error) as error:
            print("Failure", error)
        finally:
            cursor.close()
            connection.close()

def fill_table2(songs):
    """
    Fill database table with songs in one query
    """
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

    connection = None

    try:
            
        params = config()
        connection = psycopg2.connect(**params)
    
        cursor = connection.cursor()
#        print(list(song.values()))
        for song in songs:
            cursor.execute(insert_table_query, list(song.values()))
#       cursor.execute(insert_table_query, list(song.values()))
                    
        connection.commit()

    except (Exception, Error) as error:
        print("Failure", error)
    finally:
        cursor.close()
        connection.close()    

def drop_table():
    drop_table_query = "DROP TABLE IF EXISTS music"

    try:
            
            params = config()
            connection = psycopg2.connect(**params)
    
            cursor = connection.cursor()

            cursor.execute(drop_table_query)
                    
            connection.commit()

    except (Exception, Error) as error:
        print("Failure", error)
    finally:
        cursor.close()
        connection.close()



def get_from_table(limit='10'):
    songsdb = []
    get_table_query = "SELECT * FROM music ORDER BY releasedate LIMIT %s"
    
    try:
            
        params = config()
        connection = psycopg2.connect(**params)
    
        cursor = connection.cursor()

        cursor.execute(get_table_query, (limit,))
        ans = cursor.fetchall()
        ans1 = []
        for row in ans:
            
            tempdict = {
                'kind': row[1],
                'collectionName': row[2],
                'trackName': row[3],
                'collectionPrice': row[4], 
                'trackPrice': row[5], 
                'primaryGenreName': row[6], 
                'trackCount': row[7], 
                'trackNumber': row[8], 
                'releaseDate': row[9]
                }

            ans1.append(tempdict)

        connection.commit()

    except (Exception, Error) as error:
        print("Failure", error)
    finally:
        cursor.close()
        connection.close()
    
    return ans1
    
# Test Section  

#drop_table
#create_table()
#print(get_artist_id("beatles"))    
#artist_id = get_artist_id("beatles")
#songs = get_artist_songs2(artist_id, 200)

#filename = 'songs.txt'
#with open(filename, 'w') as f:
#    for song in songs:
#        f.write(songs)

#print(songs[:2])
#fill_table2(songs)

#print(get_from_table())


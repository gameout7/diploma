# import modules
import requests
import json

#Do search request with band name
band = 'abba'
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

limit = 10
itunes_lookup_link = f'https://itunes.apple.com/lookup?id={artist_id}&entity=song&limit={limit}'
#print(itunes_lookup_link)
response = requests.get(itunes_lookup_link)

temp0 = json.loads(response.content)
temp1 = temp0.get('results')
temp2 = temp1[1:] #temp is full list
songs = [] #songs is needed list

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


#print(temp2)
#print(songs)
for song in songs: #song is dict
    print(f"\n{song.get('kind', 'No value')}")
    print(song.get('collectionName', 'No value'))
    print(song.get('trackName', 'No value'))
    print(song.get('collectionPrice', 'No value'))
    print(song.get('trackPrice', 'No value'))
    print(song.get('primaryGenreName', 'No value'))
    print(song.get('trackCount', 'No value'))
    print(song.get('trackNumber', 'No value'))
    print(song.get('releaseDate', 'No value'))


#print(temp2)
#print(json.dumps(response, indent=2))
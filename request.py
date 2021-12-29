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

limit = 3
itunes_lookup_link = f'https://itunes.apple.com/lookup?id={artist_id}&entity=song&limit={limit}'
#print(itunes_lookup_link)
response = requests.get(itunes_lookup_link)

temp0 = json.loads(response.content)
temp1 = temp0.get('results')
songs = temp1[1:] #songs is list

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
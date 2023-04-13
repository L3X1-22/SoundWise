import json
import os
import io
import audio_metadata
import acoustid

apikey = 'qCWpG7ls5x'
songs = []
excepted_songs = []

def jsonSongCreator(song):
    for i in song:
        try:
            fp = acoustid.fingerprint_file(f'../Music/{i}')
            songJson = io.open(f'json_files/{i}.json', 'r')
            songJson.write(json.dumps(acoustid.lookup(apikey, fp[1], fp[0])))
            songJson.close()
        except io.UnsupportedOperation:
            print(i)
        except FileNotFoundError:
            try:
                fp = acoustid.fingerprint_file(f'../Music/{i}')
                songJson = io.open(f'json_files/{i}.json', 'w')
                songJson.write(json.dumps(acoustid.lookup(apikey, fp[1], fp[0])))
                songJson.close()
            except acoustid.FingerprintGenerationError:
                excepted_songs.append(i)
        except acoustid.FingerprintGenerationError:
            excepted_songs.append(i)
            
    

def searchNameAndArtist():
    with io.open('json_files/song.json', 'r') as f:
        data = json.load(f)

        try:
            artist = data['results'][0]['recordings'][0]['artists'][0]['name']
            song = data['results'][0]['recordings'][0]['title']

        except IndexError:
            print('ni pedo carnal, no existe esta canción jaja salu3')
            artist = None
            song = None

    print(artist, song)
    return artist, song


def searchSongs(folder):
    with os.scandir(folder) as ficheros:
        for fichero in ficheros:
            songs.append(fichero.name)

    return True
    

#jsonSongCreator()
#searchNameAndArtist()
searchSongs('../Music')
print(songs.index('Borgeous  David Solano   Big Bang (2015 Life In Color Anthem) .mp3'))
jsonSongCreator(songs)
print(excepted_songs)

'''
metadata = audio_metadata.load(test_song)
metadata['title'] = 'DJ BL3ND'
del metadata['title']
print(metadata)
'''

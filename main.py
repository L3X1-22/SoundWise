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
            
    

def searchNameAndArtist(folder):

    with os.scandir(folder) as files:
        for file in files:
            with io.open(f'json_files/{file.name}.json', 'r') as f:
                data = json.load(f)
                

                try:
                    artist = data['results'][0]['recordings'][0]['artists'][0]['name']
                    song = data['results'][0]['recordings'][0]['title']
                    print(f'file:{file.name},\n artist:{artist},\n song:{song}\n')

                except IndexError:
                    print('canción sin nombre')
                    artist = None
                    song = None

                except KeyError:
                    print('canción sin nombre')
                    artist = None
                    song = None
                except FileNotFoundError:
                    print('no existe el json')
                    artist = None
                    song = None

    print(artist, song)
    return artist, song


def searchSongs(folder):
    with os.scandir(folder) as ficheros:
        for fichero in ficheros:
            songs.append(fichero.name)

    return True
searchNameAndArtist('../Music')

'''
metadata = audio_metadata.load(test_song)
metadata['title'] = 'DJ BL3ND'
del metadata['title']
print(metadata)
'''

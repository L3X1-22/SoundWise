import json
import os
import io
import audio_metadata
import acoustid


class Song_sorter:
    def __init__(self, apikey, songs, excepted_songs, folder):
        self.folder = folder
        self.apikey = apikey
        self.songs = songs
        self.excepted_songs = excepted_songs

    def searchSongs(self, folder):
        with os.scandir(folder) as ficheros:
            for fichero in ficheros:
                self.append(fichero.name)

    def jsonSongCreator(self, song):
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
                    self.excepted_songs.append(i)

            except acoustid.FingerprintGenerationError:
                self.excepted_songs.append(i)



    def searchNameAndArtist(self, folder):

        with os.scandir(folder) as files:
            for file in files:
                try:
                    json_song = io.open(f'json_files/{file.name}.json', 'r')
                    data = json.load(json_song)


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

sorter1 = Song_sorter('qCWpG7ls5x', [], [])
'''
metadata = audio_metadata.load(test_song)
metadata['title'] = 'DJ BL3ND'
del metadata['title']
print(metadata)
'''

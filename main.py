import acoustid
import os
import io
import json
import audio_metadata



class Song_sorter:
    def __init__(self, apikey, songs, excepted_songs, folder):
        self.folder = folder
        self.apikey = apikey
        self.songs = songs
        self.excepted_songs = excepted_songs

    #this function search the songs in a folder and add them to a list
    def searchSongs(self):
        with os.scandir(self.folder) as ficheros:
            for fichero in ficheros:
                self.songs.append(fichero.name)
        return self.songs

    #this function creates JSON files for all the songs on "songs" list
    def jsonSongCreator(self, song):
        try:
            fp = acoustid.fingerprint_file(f'{self.folder}/{song}')
            songJson = io.open(f'json_files/{song}.json', 'r')
            songJson.write(json.dumps(acoustid.lookup(self.apikey, fp[1], fp[0])))
            songJson.close()

        except io.UnsupportedOperation:
            print(song)
        
        except acoustid.FingerprintGenerationError:
            self.excepted_songs.append(song)

        except FileNotFoundError:
            try:
                fp = acoustid.fingerprint_file(f'{self.folder}/{song}')
                songJson = io.open(f'json_files/{song}.json', 'w')
                songJson.write(json.dumps(acoustid.lookup(self.apikey, fp[1], fp[0])))
                songJson.close()
        
            except acoustid.FingerprintGenerationError:
                self.excepted_songs.append(song)

    #this function search and return the main artist of a song and the name of the song as well
    def searchNameAndArtist(self, song):
            try:
                json_song = io.open(f'json_files/{song}.json', 'r')
                data = json.load(json_song)
                
                try:
                    artist = data['results'][0]['recordings'][0]['artists'][0]['name']
                    name = data['results'][0]['recordings'][0]['title']
                    print(f'file:{song},\n artist:{artist},\n song:{name}\n')
                
                except IndexError:
                    print('canción sin nombre')
                    artist = None
                    name = None
                
                except KeyError:
                    print('canción sin nombre')
                    artist = None
                    name = None
                
            except FileNotFoundError:
                    print('no existe el json')
                    artist = None
                    name = None

            return [artist, name]
        
    #this functions adds the name and artist of a given song
    def metadataAdder(self, song):
        metadata = audio_metadata.load(f'{self.folder}/{song}')
        info = self.searchNameAndArtist(song)
        metadata['artist'] = info[0]
        metadata['title'] = info[1]
        print(metadata['title'], metadata['artist'])

sorter1 = Song_sorter('qCWpG7ls5x', [], [], '../Music')
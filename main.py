import os
import audio_metadata
import acoustid

test_song = './XXXTENTACION  BAD (Official Music Video).mp3'
apikey = 'qCWpG7ls5x'
json_md = os.open("./json_files/song.json", "w")

fp = acoustid.fingerprint_file(test_song)



json_md.write(acoustid.lookup(apikey, fp[1], fp[0]))

'''
metadata = audio_metadata.load(test_song)
metadata['title'] = 'DJ BL3ND'
del metadata['title']
print(metadata)
with os.scandir('../Music') as ficheros:
    for fichero in ficheros:
        print(fichero.name)
'''

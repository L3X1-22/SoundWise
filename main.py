import os
import audio_metadata
import acoustid

fp = acoustid.fingerprint_file('(PARTY MIX) - DJ BL3ND - from YouTube.mp3')
print(fp)
'''
metadata = audio_metadata.load('(PARTY MIX) - DJ BL3ND - from YouTube.mp3')
metadata['title'] = 'DJ BL3ND'
del metadata['title']
print(metadata)
with os.scandir('../Music') as ficheros:
    for fichero in ficheros:
        print(fichero.name)
'''

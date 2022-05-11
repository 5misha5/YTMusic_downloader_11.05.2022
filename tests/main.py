import eyed3
import urllib.request

filename = "Water Fountain.mp3"
#filename = "Crazy Over You.mp3"
#filename = "yes & no.mp3"
title = "Water Fountain"
artist = "Alec Benjamin"
album = "Narrated For You"
date = "2018"

audiofile = eyed3.load("Water Fountain.mp3")

audiofile.tag.title = title
audiofile.tag.artist = artist
audiofile.tag.album = album
audiofile.tag.recording_date = date
audiofile.tag.original_release_date = date



URL = 'https://i.ytimg.com/vi/WmKCEszv34A/maxresdefault.jpg'

with urllib.request.urlopen(URL) as url:
    with open('photo.jpg', 'wb') as f:
        f.write(url.read())

audiofile.tag.images.set(3, open("photo.jpg", 'rb').read(), 'image/jpeg')

audiofile.tag.save(version=eyed3.id3.ID3_V2_3)


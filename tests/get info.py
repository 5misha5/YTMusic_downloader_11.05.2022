from ytmusicapi import YTMusic
import json


id = "WmKCEszv34A"
#id = "rIL3FSz6qDY"
#id = "3PPaFmI08GY"
#id = "Gy_ExjhjA-4"
#id = "qeMFqkcPYcg"
#ytmusic = YTMusic.__init__()
info = YTMusic.get_song(YTMusic(),id)
image_url = info["microformat"]["microformatDataRenderer"]["thumbnail"]["thumbnails"][0]["url"]
tags = info["microformat"]["microformatDataRenderer"]["tags"]
title = info["videoDetails"]["title"]
artist = info["videoDetails"]["author"]
date = info["microformat"]["microformatDataRenderer"]["publishDate"]
print(date, title, artist)
print(image_url)
'''with open("{title}.json".format(title = title), "w") as file:
    json.dump(info, file, indent=4, sort_keys=True)
#print(YTMusic.get_lyrics(YTMusic(), id))'''
from pytube import Playlist, extract, YouTube
from ytmusicapi import YTMusic
import yt_dlp
import eyed3
import urllib.request
import moviepy.editor as mp
from os.path import exists
import os
from retry import retry

import get_album_id



headers = '''{
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "X-Goog-AuthUser": "0",
        "x-origin": "https://music.youtube.com",
        "Cookie" : "VISITOR_INFO1_LIVE=ERGVNrI_klM; _gcl_au=1.1.1521483703.1663076014; _ga=GA1.1.996066172.1663076019; PREF=tz=Europe.Kiev&f6=40000000&autoplay=true&library_tab_browse_id=FEmusic_liked_playlists; YSC=Zi4Q-RGj_b4; SID=OggjtWJII4fNAE7buaPybFqV07v76kOCcK2s-XuCe8B0X7gWooyjY_eKPSPVS5YskxqHlA.; __Secure-1PSID=OggjtWJII4fNAE7buaPybFqV07v76kOCcK2s-XuCe8B0X7gWs8SEH83RGKmtIxy7mzimOQ.; __Secure-3PSID=OggjtWJII4fNAE7buaPybFqV07v76kOCcK2s-XuCe8B0X7gWizhew91UDBzlyFAq-llScw.; HSID=AVhcHvU8b2d-KH1k5; SSID=AyePmXDD8hO2FR8TG; APISID=oIIfVkc928RU_K4Z/AqYn3Y4g7kxLu_w6X; SAPISID=z2Du3A8WKPjN6Uol/A28IXGtZJwDKwVhj9; __Secure-1PAPISID=z2Du3A8WKPjN6Uol/A28IXGtZJwDKwVhj9; __Secure-3PAPISID=z2Du3A8WKPjN6Uol/A28IXGtZJwDKwVhj9; LOGIN_INFO=AFmmF2swRQIhAL9OyAVyvwUPHq1sCTUmOpEXExkxj81UQp27ZPGnZCjkAiB4OGGK3_0XLEfIC_U5VHVNoz0YF2Yr_azWV8AHoPt_8w:QUQ3MjNmd1pSWUR2RDNRbWJqUDRUSE1TdkRJMVlBdzV6ZXk3TXpLVnEtSzVPd1pTNHZzb0ptWjBucWZDRUVvWW42X0dqaGd4RUQwM2NDRnV1eHFxT3RySXRFS2VjUGQ1QzRrdjZTVzdXOWxNVkhaaC1DT1ZBOWFjNU42VE5VY25fSi1DZGtETW1yazRhUnFIRkcyRlg5RG1iVVBDNGRZd3FR; SIDCC=AEf-XMQYb_qCqq13Tj0uBrVLZyZTL2JmNRirQGHHjc_FPAinWqcl7rZnYDSKPEehl2Q2NFae; __Secure-1PSIDCC=AEf-XMT0EYHhOuFVslKiNhcO27twVdLzT11Z__whlN8FSGlwTGlgyg2DRRIdS549HPP5YF-cpA; __Secure-3PSIDCC=AEf-XMTOik_G-3ILgGpgbYoyLhSbO0-4IjSq4TwNvmWKi546RfH_QlOTtFoVkVkD6r6rzs0Zug; _ga_VCGEPY40VB=GS1.1.1663247067.17.1.1663247705.0.0.0"
    }'''

class Song():


    def __init__(self, video_url = None, video_id = None) -> None:

        if not video_url:
            self.id = video_id
            self.url = f"https://youtu.be/{self.id}"
        elif not video_id:
            self.url = video_url
            self.id = extract.video_id(self.url)
        else:
            raise "Expected only video_url or video_id"
        
        self.ytm = YTMusic()
        
        self.info = self.get_info()

        self.album = self.get_album()

        self.title = self.get_title()
        self.artist = self.get_artist()
        
        self.date = self.get_date()
        self.thumbnail_url = self.get_thumbnail_url()


    def get_info(self):
        info = self.ytm.get_song(self.id)
        return info

    def get_title(self):
        title = ""
        try:
            title =  yt_dlp.YoutubeDL().extract_info(
                url = self.url,download=False
                )['title']
        except: pass
        try:
            title = self.info["videoDetails"]["title"]
        except: pass
        return title

    def get_artist(self):
        artist = ""
        try:
            artist = self.info["videoDetails"]["author"]
        except: pass
        return artist
    def get_album(self):
        album_name = "" 
        album_id = get_album_id.get(self.id)

        if album_id:
            album_name = self.ytm.get_album(album_id)["title"]
            
        return album_name
    def get_date(self):
        date = ""
        try:
            date = self.info["microformat"]["microformatDataRenderer"]["publishDate"]
        except Exception as e: print("You have some error", e)
        return date
    def get_thumbnail_url(self):
        thumbnail_url = ""
        thumbnail_url = YouTube(self.url).thumbnail_url
        try: 
            thumbnail_url = self.info["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
        except: pass

        return thumbnail_url

    def get_filename(self):
        filename = ""
        for i in self.title:
            if not i in '/|:*?"<\>':
                filename += i
        return filename + f" {self.id}"
    


    def download(self, path = "music"):
            
        filename = self.get_filename()
        video_path = "temp/{filename}.mp4".format(filename = filename)
        audiofile_name = "{filename}.mp3".format(filename = filename)
        audiofile_path = "{path}/{filename}.mp3".format(filename = filename, path = path)
        while not exists(audiofile_path):

            with yt_dlp.YoutubeDL({'outtmpl':video_path}) as ydl:
                ydl.download([self.url])
            
            #get audio
            my_clip = mp.VideoFileClip(video_path)

            if exists(audiofile_path):
                continue

            audiofile = my_clip.audio.write_audiofile(audiofile_name)

            #adding tags
            audiofile = eyed3.load(audiofile_name)
            
            
            audiofile.tag.title = self.title
            try:
                audiofile.tag.artist = self.artist
                audiofile.tag.album = self.album
                audiofile.tag.recording_date = self.date
                audiofile.tag.original_release_date = self.date
            except: pass


            with urllib.request.urlopen(self.thumbnail_url) as url:
                with open('temp/thumbnail.jpg', 'wb') as f:
                    f.write(url.read())

            audiofile.tag.images.set(3, open("temp/thumbnail.jpg", 'rb').read(), 'image/jpeg')

            audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

            os.replace(audiofile_name, audiofile_path)
    def print_info(self):
        print("title:", self.title)
        print("artist:", self.artist)
        print("album:", self.album)
        print("date:", self.date)
        print("thumbnail_url:", self.thumbnail_url)

class Playlist():
    def __init__(self, playlist_url = None, playlist_id = None, ytm=YTMusic()) -> None:

        if not playlist_url:
            self.id = playlist_id
            self.url = f"https://music.youtube.com/playlist?list={self.id}"
        elif not playlist_id:
            self.url = playlist_url
            self.id = extract.playlist_id(self.url)
        else:
            raise "Expected only playlist_url or playlist_id"
        
        self.tracks = ytm.get_playlist('LM', 1000)["tracks"]
        self.videos_id = [track["videoId"] for track in self.tracks]
        
    
    def download(self) -> None:
        for video_id in self.videos_id:
            Song(video_id=video_id).download()

if __name__ == "__main__":

    

    headers = '''{
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "X-Goog-AuthUser": "0",
        "x-origin": "https://music.youtube.com",
        "Cookie" : "VISITOR_INFO1_LIVE=ERGVNrI_klM; _gcl_au=1.1.1521483703.1663076014; _ga=GA1.1.996066172.1663076019; PREF=tz=Europe.Kiev&f6=40000000&autoplay=true&library_tab_browse_id=FEmusic_liked_playlists; YSC=Zi4Q-RGj_b4; SID=OggjtWJII4fNAE7buaPybFqV07v76kOCcK2s-XuCe8B0X7gWooyjY_eKPSPVS5YskxqHlA.; __Secure-1PSID=OggjtWJII4fNAE7buaPybFqV07v76kOCcK2s-XuCe8B0X7gWs8SEH83RGKmtIxy7mzimOQ.; __Secure-3PSID=OggjtWJII4fNAE7buaPybFqV07v76kOCcK2s-XuCe8B0X7gWizhew91UDBzlyFAq-llScw.; HSID=AVhcHvU8b2d-KH1k5; SSID=AyePmXDD8hO2FR8TG; APISID=oIIfVkc928RU_K4Z/AqYn3Y4g7kxLu_w6X; SAPISID=z2Du3A8WKPjN6Uol/A28IXGtZJwDKwVhj9; __Secure-1PAPISID=z2Du3A8WKPjN6Uol/A28IXGtZJwDKwVhj9; __Secure-3PAPISID=z2Du3A8WKPjN6Uol/A28IXGtZJwDKwVhj9; LOGIN_INFO=AFmmF2swRQIhAL9OyAVyvwUPHq1sCTUmOpEXExkxj81UQp27ZPGnZCjkAiB4OGGK3_0XLEfIC_U5VHVNoz0YF2Yr_azWV8AHoPt_8w:QUQ3MjNmd1pSWUR2RDNRbWJqUDRUSE1TdkRJMVlBdzV6ZXk3TXpLVnEtSzVPd1pTNHZzb0ptWjBucWZDRUVvWW42X0dqaGd4RUQwM2NDRnV1eHFxT3RySXRFS2VjUGQ1QzRrdjZTVzdXOWxNVkhaaC1DT1ZBOWFjNU42VE5VY25fSi1DZGtETW1yazRhUnFIRkcyRlg5RG1iVVBDNGRZd3FR; SIDCC=AEf-XMQYb_qCqq13Tj0uBrVLZyZTL2JmNRirQGHHjc_FPAinWqcl7rZnYDSKPEehl2Q2NFae; __Secure-1PSIDCC=AEf-XMT0EYHhOuFVslKiNhcO27twVdLzT11Z__whlN8FSGlwTGlgyg2DRRIdS549HPP5YF-cpA; __Secure-3PSIDCC=AEf-XMTOik_G-3ILgGpgbYoyLhSbO0-4IjSq4TwNvmWKi546RfH_QlOTtFoVkVkD6r6rzs0Zug; _ga_VCGEPY40VB=GS1.1.1663247067.17.1.1663247705.0.0.0"
    }'''

    user_id = "114293612117065396076"

    ytm = YTMusic(auth = headers, user = user_id)

    tracks = ytm.get_playlist('LM', 1000)["tracks"]

    for track in tracks:
        song = Song(video_id = track["videoId"])
        song.print_info()
        #song.download()

        #Song(track["videoId"]).download()
    
    

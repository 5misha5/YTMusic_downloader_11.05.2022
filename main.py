from pytube import Playlist, extract, YouTube
from ytmusicapi import YTMusic
import youtube_dl
import eyed3
import urllib.request
import moviepy.editor as mp
from os.path import exists
import os

#get playlist's video urls
#p = Playlist(input("Enter YTMusic playlist url: "))

p = Playlist("https://music.youtube.com/playlist?list=PLCRUvzR-tXCjM-a0VA7NjzttQ4CQPj8CJ&feature=share")

downloaded_videos = []

not_downloaded_urls = open("not_downloaded_urls.txt","w")
try:
    os.mkdir(os.path.join("", "music"))
except:
    pass


for video_url in list(p.video_urls)[-10:]:   
    try:

        video_info = youtube_dl.YoutubeDL().extract_info(
            url = video_url,download=False
            )
        title = f"{video_info['title']}"
        image_url = ""
        artist = ""
        date = ""
        image_url = YouTube(video_url).thumbnail_url

        #extracting information
        try:
            id = extract.video_id(video_url)
            info = YTMusic.get_song(YTMusic(),id)
            image_url = info["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
        except: pass
        try:
            tags = info["microformat"]["microformatDataRenderer"]["tags"]
            title = info["videoDetails"]["title"]
            artist = info["videoDetails"]["author"]
            date = info["microformat"]["microformatDataRenderer"]["publishDate"]
        except: pass

        filename = ""
        for i in title:
            if not i in "/|":
                filename += i
        print(video_url)
        print(title)
        print(artist)
        print(date)
        
        #downloading video
        video_path = "video/{filename}.mp4".format(filename = filename)
        audiofile_name = "{filename}.mp3".format(filename = filename)
        audiofile_path = "music/{filename}/{filename}.mp3".format(filename = filename)

        #while music not downloaded
        while not exists(audiofile_path):

            with youtube_dl.YoutubeDL({'outtmpl':video_path,}) as ydl:
                ydl.download([video_url])

            
            #get audio
            my_clip = mp.VideoFileClip(video_path)

            if exists(audiofile_path):
                continue

            audiofile = my_clip.audio.write_audiofile(audiofile_name)

            #adding tags
            audiofile = eyed3.load(audiofile_name)
            
            
            audiofile.tag.title = title
            try:
                audiofile.tag.artist = artist
                audiofile.tag.recording_date = date
                audiofile.tag.original_release_date = date
            except: pass


            with urllib.request.urlopen(image_url) as url:
                with open('photo.jpg', 'wb') as f:
                    f.write(url.read())

            audiofile.tag.images.set(3, open("photo.jpg", 'rb').read(), 'image/jpeg')

            audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

            try:
                os.mkdir(os.path.join("music", filename))
            except:
                pass

            os.replace(audiofile_name, audiofile_path)


            #AUDIT

        downloaded_videos.append(video_url)
        
    except Exception as error:
        not_downloaded_urls.write(video_url + "\n")
        print("YOU HAVE SOME ERROR with some url: {url}\n{error}".format(error=error, url=video_url))


print(len(p.video_urls)-len(downloaded_videos))
for not_downloaded_video in set(p.video_urls)-set(downloaded_videos):
    print(not_downloaded_video)
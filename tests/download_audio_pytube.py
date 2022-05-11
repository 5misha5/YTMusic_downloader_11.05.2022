# importing packages
from pytube import YouTube
  
# url input from user
url = "https://music.youtube.com/watch?v=WmKCEszv34A&feature=share"
yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')

title = yt.title
image_url = yt.thumbnail_url

print(image_url)

type(yt.streams)

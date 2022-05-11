import youtube_dl

video_url = input("please enter youtube video url:")
video_info = youtube_dl.YoutubeDL().extract_info(
        url = video_url,download=False
    )

filename = "video.mp4"

with youtube_dl.YoutubeDL({'outtmpl':filename}) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
from pytubefix import YouTube

yt = YouTube(
    "https://www.youtube.com/watch?v=1yvBqasHLZs",
    proxies=dict(https="http://127.0.0.1:8118"),
)
# print(yt.captions)
# print(yt.title)

ys = yt.streams.get_audio_only()
if ys is not None:
    ys.download()

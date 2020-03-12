from gitdir import gitdir as gd

def update():
    url = "https://github.com/ytdl-org/youtube-dl/tree/master/youtube_dl/"
    f = open("files")
    for x in f:
        gd.download(url + x[:-1], False)

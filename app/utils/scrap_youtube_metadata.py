from typing import TypedDict

import pytube

pytube.innertube._default_clients['ANDROID']=pytube.innertube._default_clients['WEB']


class YoutubeMetadata(TypedDict):
    title: str
    author: str
    description: str
    thumbnail_url: str

def scrap_youtube_metadata(youtube_id: str) -> YoutubeMetadata:
    yt = pytube.YouTube(f"https://www.youtube.com/watch?v={youtube_id}")
    return {
        "title": yt.title,
        "author": yt.author,
        "description": yt.description,
        "thumbnail_url": yt.thumbnail_url
    }

if __name__ == "__main__":
    print(scrap_youtube_metadata("QXeEoD0pB3E"))
from typing import TypedDict

from pytube import YouTube


class YoutubeMetadata(TypedDict):
    title: str
    author: str
    description: str

def scrap_youtube_metadata(youtube_id: str) -> YoutubeMetadata:
    yt = YouTube(f"https://www.youtube.com/watch?v={youtube_id}")
    return {
        "title": yt.title,
        "author": yt.author,
        "description": yt.description,
    }

if __name__ == "__main__":
    print(scrap_youtube_metadata("QXeEoD0pB3E"))
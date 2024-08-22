from youtube_transcript_api import YouTubeTranscriptApi as yta
from langchain_core.documents import Document
from typing import List

def scrap_youtube_transcript(youtube_id: str) -> (List[Document], str):
    try:
        transcript = yta.get_transcript(youtube_id)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    transcript_list = []
    plain_transcript = ""
    for entry in transcript:
        text = entry['text']
        start = entry['start']
        duration = entry['duration']
        
        # Convert start time to HH:MM:SS format
        hours, remainder = divmod(start, 3600)
        minutes, seconds = divmod(remainder, 60)
        timestamp = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        plain_transcript += text + " "
        
        new_transcript = {"text": text, "start": start, "duration": duration, "timestamp": timestamp}
        transcript_list.append(new_transcript)
        
    return transcript_list, plain_transcript

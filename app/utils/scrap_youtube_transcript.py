from typing import List

from fastapi import HTTPException
from langchain_core.documents import Document
from youtube_transcript_api import YouTubeTranscriptApi as yta


def scrap_youtube_transcript(youtube_id: str) -> tuple[List[Document], str]:
    try:
        transcript = yta.get_transcript(youtube_id)
    except Exception as e:
        # Log the error details (optional)
        print(f"An error occurred while fetching transcript for {youtube_id}: {e}")
        
        # Raise an HTTPException with a 500 Internal Server Error status
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching the transcript. This video might not  have a transcript available. "+str(e)
        )

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

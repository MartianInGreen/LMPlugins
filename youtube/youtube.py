import json
from pytube import YouTube 
from youtube_transcript_api import YouTubeTranscriptApi

def lambda_handler(event, context):
    # See if body is json or load json from string
    try:
        body = event["body"]
        video_id = body["video_id"]
    except:
        body = json.loads(event["body"])
        video_id = body["video_id"]

    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    text = []
    for part in transcript:
        text.append(part['text'])
    
    return {
        'title': yt.title,
        'channel': yt.author,
        'description': yt.description,
        'length': str(yt.length) + " s",
        'views': yt.views,
        'transcription': text
    }
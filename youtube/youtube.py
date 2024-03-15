import json
from youtube_transcript_api import YouTubeTranscriptApi

def lambda_handler(event, context):
    # See if body is json or load json from string
    try:
        body = event["body"]
        video_id = body["video_id"]
    except:
        body = json.loads(event["body"])
        video_id = body["video_id"]

    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    text = []
    for part in transcript:
        text.append(part['text'])
    
    return {text}
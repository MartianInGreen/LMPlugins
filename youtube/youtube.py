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

    print(f"Getting video with id: {video_id}")
    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')

    # Get avalilbe languages
    languages_raw = YouTubeTranscriptApi.list_transcripts(video_id)
    languages = []

    for lang in languages_raw:
        languages.append(lang.language_code)
    print(f"Available languages: {languages}")

    # Get transcript (get english by default, if not available get first language)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[languages[0]])
    
    text = []
    for part in transcript:
        text.append(part['text'])

    i: int = yt.watch_html.find('"shortDescription":"')
    desc: str = '"'
    i += 20  # excluding the `"shortDescription":"`
    while True:
        letter = yt.watch_html[i]
        desc += letter  # letter can be added in any case
        i += 1
        if letter == '\\':
            desc += yt.watch_html[i]
            i += 1
        elif letter == '"':
            break
    
    return {
        'title': yt.title,
        'channel': yt.author,
        'description': desc,
        'length': str(yt.length) + " s",
        'views': yt.views,
        'transcription': text
    }
import json
import os
import re
import ssl
import urllib.parse
import urllib.request

from youtube_transcript_api import YouTubeTranscriptApi

try:
    import certifi
except ImportError:  # pragma: no cover
    certifi = None


def _youtube_api_request(params: dict) -> dict:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY is missing. Add it to your .env file.")

    params = {**params, "key": api_key}
    url = "https://www.googleapis.com/youtube/v3/" + params.pop("endpoint") + "?" + urllib.parse.urlencode(params)
    context = ssl.create_default_context(cafile=certifi.where()) if certifi is not None else ssl.create_default_context()
    with urllib.request.urlopen(url, context=context) as response:
        return json.loads(response.read().decode("utf-8"))


def get_channel_id(channel_handle: str) -> str:
    data = _youtube_api_request({
        "endpoint": "channels",
        "part": "id",
        "forHandle": channel_handle,
    })
    items = data.get("items", [])
    if not items:
        raise ValueError(f"No channel found for handle {channel_handle}.")
    return items[0]["id"]


def fetch_broadcasts(channel_handle: str, max_results: int = 14) -> list[dict]:
    channel_id = get_channel_id(channel_handle)

    search_params = {
        "endpoint": "search",
        "part": "id,snippet",
        "channelId": channel_id,
        "type": "video",
        "order": "date",
        "maxResults": max_results,
    }

    # Some channels have no currently live broadcasts. In that case, fall back to the latest
    # recent videos for the channel so the selector is never empty for a valid channel.
    for params in (
        {**search_params, "eventType": "live"},
        search_params,
    ):
        data = _youtube_api_request(params)
        videos = []
        for item in data.get("items", []):
            video_id = item["id"].get("videoId")
            if video_id:
                videos.append({
                    "video_id": video_id,
                    "title": item["snippet"].get("title", "Untitled video"),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "published_at": item["snippet"].get("publishedAt", ""),
                })
        if videos:
            return videos

    return []

def fetch_transcript(video_url: str) -> str:
    """Fetches the transcript for a given YouTube video URL."""
    
    # 11 chars after 'v=' in the URL is the video ID
    video_id = video_url.split('v=')[1][:11]
    
    # create YT object and fetch transcript
    yt = YouTubeTranscriptApi()
    transcripts = yt.list(video_id=video_id)
    if not transcripts:
        raise RuntimeError("No transcripts available for this video")
    
    # get first language code and fetch transcript
    lang_code = list(transcripts)[0].language_code
    transcript_obj = transcripts.find_transcript([lang_code])
    transcript_data = transcript_obj.fetch()
    
    full_transcript_text = " ".join([entry.text for entry in transcript_data])
    
    return full_transcript_text

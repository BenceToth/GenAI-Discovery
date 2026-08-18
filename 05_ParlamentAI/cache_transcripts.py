"""Run this locally (from a non-cloud IP) to refresh the transcript cache.

YouTube blocks transcript fetches from cloud-provider IPs, so the Space can't fetch
transcripts live. Instead, run this script from your own machine periodically, then
commit and push the updated transcripts/ folder so the Space can read from it.
"""
import os

from dotenv import load_dotenv

from youtube_scraper import fetch_broadcasts, fetch_transcript

BASE_DIR = os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)

CHANNEL_HANDLE = "@OrszaggyulesELO"


def main():
    videos = fetch_broadcasts(CHANNEL_HANDLE, max_results=14)
    for video in videos:
        try:
            fetch_transcript(video["url"])
            print(f"Cached: {video['video_id']} - {video['title']}")
        except Exception as e:
            print(f"Failed:  {video['video_id']} - {video['title']}: {e}")


if __name__ == "__main__":
    main()

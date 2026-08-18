import os
import re
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import gradio as gr

from youtube_scraper import fetch_broadcasts, fetch_transcript


# Load APIs from .env
BASE_DIR = os.path.dirname(__file__)
PARENT_ENV = os.path.join(os.path.dirname(BASE_DIR), ".env")
load_dotenv(dotenv_path=PARENT_ENV, override=True)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

if not YOUTUBE_API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY not found in environment. Please create a .env file with the key.")

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN not found in environment. Please create a .env file with a Hugging Face access token.")

# Hugging Face's Inference Providers router exposes an OpenAI-compatible API,
# so the same OpenAI SDK works here - only the base_url, key, and model change.
client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=HF_TOKEN)
MODEL_HF = "meta-llama/Llama-3.1-8B-Instruct"

# YouTube channel to fetch videos from. This is the official channel of the Hungarian Parliament.
CHANNEL_HANDLE = "@OrszaggyulesELO"

def generate_minutes(transcript: str):
    system_message = (
        "You produce minutes of meetings from transcripts. "
        "Write a concise markdown summary with sections for summary, discussion points, takeaways, and action items with owners. "
        "Do not invent dates, deadlines, attendees, or meeting metadata. "
        "Only include a date or deadline if the transcript explicitly provides it. "
        "If it is not present, omit it entirely. Do not use placeholders such as [insert date] or [insert deadline]."
    )

    user_prompt = f"""
Below is an extract transcript of a Hungarian Parliament meeting (in Hungarian Language).
Create a professional meeting minutes document in English, without code blocks.

Requirements:
- Summary with attendees only if clearly mentioned in the transcript
- Discussion points
- Takeaways
- Action items with owners only when explicitly stated
- Include date/deadline only if explicitly mentioned in the transcript; otherwise omit it completely
- Never use placeholders such as [insert date], [insert deadline], or similar text

Transcription:
{transcript}
"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt},
    ]

    # Use streaming API to yield partial content as it's produced by the model
    stream = client.chat.completions.create(model=MODEL_HF, messages=messages, max_tokens=1500, temperature=0.2, stream=True)
    collected = ""
    for chunk in stream:
        # Each chunk may contain a delta with content
        try:
            delta = chunk.choices[0].delta
            text = getattr(delta, "content", None)
        except Exception:
            # fallback for dict-like chunk
            try:
                text = chunk["choices"][0]["delta"].get("content", "")
            except Exception:
                text = ""
        if text:
            collected += text
            yield text


def load_video_choices(channel_handle: str):
    """Fetches the latest live broadcasts for a given YouTube channel handle and returns a list of choices for a dropdown menu."""
    try:
        videos = fetch_broadcasts(channel_handle, max_results=14)
        choices = [v['title'] for v in videos]
        selected = videos[0]["video_id"]
        return gr.update(choices=choices, value=selected, visible=True), gr.update(value=f"Loaded {len(videos)} live videos.", visible=True)
    except Exception as e:
        return gr.update(choices=[], value=None, visible=False), gr.update(value=f"Error loading videos: {e}", visible=True)


def summarize_url(video_id: str):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    yield gr.update(visible=True, value="Fetching transcript..."), ""
    try:
        transcript = fetch_transcript(video_url)

    except Exception as e:
        yield gr.update(visible=True, value=f"Error fetching transcript: {e}"), ""
        return

    # Generate minutes and stream back results
    yield gr.update(visible=True, value="Generating minutes (this may take a moment)..."), ""
    try:
        minutes_parts = []
        for part in generate_minutes(transcript):
            if part is None:
                continue
            if isinstance(part, str):
                minutes_parts.append(part)
                yield gr.update(visible=True, value="Generating minutes (in progress)"), "".join(minutes_parts)
    except Exception as e:
        yield gr.update(visible=True, value=f"Error generating minutes: {e}"), ""
        return

    final_minutes = "".join(minutes_parts)
    yield gr.update(visible=True, value="Done"), final_minutes


def build_ui():
    videos = fetch_broadcasts(CHANNEL_HANDLE, max_results=14)
    initial_choices = [(v['title'], v['video_id']) for v in videos]

    with gr.Blocks(title="ParlamentAI Minutes Generator") as iface:
        gr.Markdown("# ParlamentAI Minutes Generator")
        gr.Markdown("Latest recent videos from @OrszaggyulesELO")
        gr.Markdown(f"_Powered by the open-source model `{MODEL_HF}` via Hugging Face Inference Providers._")

        with gr.Row():
            with gr.Column(scale=1):
                video_select = gr.Dropdown(label="Select a video", choices=initial_choices, value=initial_choices[0][1])
                status_box = gr.Textbox(label="Status", interactive=False)
                submit_btn = gr.Button("Generate Summary", variant="primary")

            with gr.Column(scale=2):
                summary_box = gr.Markdown(label="Minutes")

        submit_btn.click(fn=summarize_url, inputs=video_select, outputs=[status_box, summary_box])

    return iface

if __name__ == "__main__":
    app = build_ui()
    app.launch()

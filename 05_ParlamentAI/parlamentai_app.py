import os
import re
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import gradio as gr


# Load environment from parent directory (matches notebook behavior)
BASE_DIR = os.path.dirname(__file__)
PARENT_ENV = os.path.join(os.path.dirname(BASE_DIR), ".env")
load_dotenv(dotenv_path=PARENT_ENV, override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in environment. Please create a .env file with the key.")

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL_GPT = "gpt-4o-mini"


def extract_video_id(url: str) -> str:
    """Extract YouTube video id from a URL or return the text if it's already an id."""
    if not url:
        raise ValueError("Empty URL")
    # Original notebook logic: take 11 chars after 'v='
    if 'v=' in url:
        idx = url.split('v=')[1]
        return idx[:11]
    # fallback: if it's already 11 chars assume it's the id
    if len(url.strip()) == 11:
        return url.strip()
    raise ValueError("Could not extract a YouTube video id from the provided URL. Provide a URL containing 'v=' or the 11-char id.")


def fetch_transcript(video_url: str) -> str:
    video_id = extract_video_id(video_url)
    yt = YouTubeTranscriptApi()
    transcripts = yt.list(video_id=video_id)
    if not transcripts:
        raise RuntimeError("No transcripts available for this video")
    
    # get first language code and fetch transcript
    lang_code = list(transcripts)[0].language_code
    transcript_obj = transcripts.find_transcript([lang_code])
    transcript_data = transcript_obj.fetch()
    
    full_transcript_text = " ".join([entry.text for entry in transcript_data])
    
    # limit size to avoid token issues
    if len(full_transcript_text) > 12000:
        full_transcript_text = full_transcript_text[:12000] + "\n\n[Truncated transcript due to length]"
    return full_transcript_text


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
    stream = client.chat.completions.create(model=MODEL_GPT, messages=messages, max_tokens=1500, temperature=0.2, stream=True)
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


def summarize_url(url: str):
    # This function is a generator to stream updates to the UI.
    if not url:
        yield gr.update(visible=True, value="Please enter a YouTube URL or video id."), ""
        return

    # Show status field only after the button click starts the process
    yield gr.update(visible=True, value="Fetching transcript..."), ""
    try:
        transcript = fetch_transcript(url)
    except Exception as e:
        yield gr.update(visible=True, value=f"Error fetching transcript: {e}"), ""
        return

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
    with gr.Blocks(title="ParlamentAI Minutes Generator") as iface:
        gr.Markdown("# ParlamentAI Minutes Generator")
        gr.Markdown("Enter a YouTube URL to fetch the transcript and generate meeting minutes.")

        with gr.Row():
            with gr.Column(scale=1):
                url_input = gr.Textbox(lines=1, placeholder="Enter YouTube URL or video id", label="YouTube URL")
                status_box = gr.Textbox(label="Status", interactive=False, visible=False)
                submit_btn = gr.Button("Generate Summary", variant="primary")

            with gr.Column(scale=2):
                summary_box = gr.Markdown(label="Minutes")

        submit_btn.click(fn=summarize_url, inputs=url_input, outputs=[status_box, summary_box])

    return iface

if __name__ == "__main__":
    app = build_ui()
    app.launch()

# ParlamentAI

ParlamentAI is a small workflow for fetching Hungarian parliamentary YouTube videos, extracting transcripts, and generating concise meeting minutes with OpenAI. The project includes a notebook, a scraper utility, and a Gradio web app.

## Project files

- `parlamentai.ipynb` — notebook-based exploration and prototype workflow.
- `youtube_scraper.py` — fetches YouTube channel video metadata and transcript text.
- `parlamentai_app.py` — Gradio interface for selecting a parliament video and generating a summary.
- `requirements.txt` — Python dependencies for the notebook, scraper, and app.

## Features

- Query a YouTube channel for recent broadcast or upload videos.
- Extract a video transcript from YouTube using `youtube-transcript-api`.
- Summarize the transcript into meeting minutes with `gpt-4o-mini`.
- View the generated output in a simple Gradio UI.
- Keep the workflow focused on the official Hungarian Parliament channel `@OrszaggyulesELO`.

## Environment variables

Create a `.env` file in the parent project directory, next to this folder, with:

```env
OPENAI_API_KEY=sk-...
YOUTUBE_API_KEY=YOUR_YOUTUBE_DATA_API_KEY
```

## Install dependencies

```bash
cd Udemy_Agentic-AI/GenAI-Discovery/05_ParlamentAI
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run the notebook

Open `parlamentai.ipynb` in VS Code or Jupyter and run the cells in order.

## Run the Gradio app

From the project directory:

```bash
python parlamentai_app.py
```

Then open the local URL printed in the terminal, usually:

```text
http://127.0.0.1:7861
```

## How the scraper works

`youtube_scraper.py`:

- looks up the channel ID from a handle such as `@OrszaggyulesELO`
- searches for recent live broadcasts or recent videos
- returns titles, video IDs, and URLs
- extracts transcript text for the selected video

## Security and secret handling

- Never commit `.env` files to version control.
- Do not commit notebooks or terminal output that contains API keys.
- Rotate keys immediately if they are exposed accidentally.

## Troubleshooting

- If the selector is empty, confirm that `YOUTUBE_API_KEY` is present and valid.
- If transcripts fail, confirm the YouTube video has an available transcript.
- If the OpenAI call fails, verify that `OPENAI_API_KEY` is valid and has sufficient quota.

## Related files

- `youtube_scraper.py` — data-fetching utility
- `parlamentai_app.py` — web UI
- `parlamentai.ipynb` — notebook prototype

<img width="1224" height="685" alt="image" src="https://github.com/user-attachments/assets/692e48be-6ef1-408b-b2ce-5561d7224bef" />

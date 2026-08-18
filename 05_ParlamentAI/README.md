# ParlamentAI

Try the live demo on Hugging Face Spaces: https://huggingface.co/spaces/BenToT360/ParlamentAI

ParlamentAI is a small workflow for fetching Hungarian parliamentary YouTube videos, extracting transcripts, and generating concise meeting minutes with OpenAI. The project includes a notebook, a scraper-based prototype, and lightweight web UIs for local and hosted demos.

## Project files

- `parlamentai.ipynb` — notebook-based exploration and prototype workflow.
- `youtube_scraper.py` — fetches YouTube channel video metadata and transcript text.
- `parlamentai_app.py` — Gradio interface for selecting a parliament video and generating a summary.
- `requirements.txt` — Python dependencies for the notebook, scraper, and app.

## Features

- Query a YouTube channel for recent broadcast or upload videos.
- Extract a video transcript from YouTube using `youtube-transcript-api`.
- Summarize the transcript into meeting minutes with `gpt-4o-mini` (or an open-source HF model in the Spaces demo).
- View the generated output in a simple Gradio UI.
- Keep the workflow focused on the official Hungarian Parliament channel `@OrszaggyulesELO`.

## Hugging Face Space (open demo)

A Hugging Face Spaces variant of this app has been added so anyone can try ParlamentAI with an open-source model hosted on the Hugging Face Hub. The Space runs a lightweight Gradio app configured to use an open-source text-generation model (no OpenAI key required for the public demo).

Key notes:

- Try the demo on Hugging Face Spaces once the project Space is deployed (the public Space URL will be added here when available).
- The HF Space uses an open-source model from the Hugging Face Hub to perform text generation/summary tasks so the demo remains freely accessible.
- There is an `hf_space/` folder in the repo (if present) that contains the Space entrypoint and dependency hints. The Space entrypoint and dependency file (for example `app.py` and `requirements.txt`) mirror the local Gradio app but are tuned to use an HF model.
- If you want to run the same app locally against an open-source HF model, ensure you have the required dependencies and set any model-specific environment variables (for example, `HF_HUB_API_TOKEN` if you need access to a private model or API-backed runtime).

## Environment variables

Create a `.env` file in the parent project directory, next to this folder, with:

```env
OPENAI_API_KEY=sk-...
YOUTUBE_API_KEY=YOUR_YOUTUBE_DATA_API_KEY
```

For the Hugging Face variant you may also set (only if required by the chosen model/runtime):

```env
HF_HUB_API_TOKEN=hf_...
```

## Install dependencies

```bash
cd Udemy_Agentic-AI/GenAI-Discovery/05_ParlamentAI
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If you're running the Hugging Face Space locally from an `hf_space/` folder, check for a separate `requirements.txt` there and install it instead.

## Run the notebook

Open `parlamentai.ipynb` in VS Code or Jupyter and run the cells in order.

## Run the Gradio app (local)

From the project directory:

```bash
python parlamentai_app.py
```

Then open the local URL printed in the terminal, usually:

```text
http://127.0.0.1:7861
```

## Run the Hugging Face Space variant locally

If you want to run the HF-ready app variant locally (for example to test with an open-source HF model) run the same Gradio script or the Space-specific entrypoint used in the `hf_space/` folder (if present). Typical steps:

```bash
# from the repo root or hf_space folder
python app.py  # or the Space entrypoint file
```

Open the local URL printed in the terminal and test the same workflow.

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
- `hf_space/` — optional Hugging Face Space entrypoint and dependency files (when present)

<img width="1224" height="685" alt="image" src="https://github.com/user-attachments/assets/692e48be-6ef1-408b-b2ce-5561d7224bef" />

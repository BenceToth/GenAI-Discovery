# ParlamentAI Notebook

A Jupyter notebook that fetches a YouTube transcript of a Hungarian parliamentary session and uses OpenAI to produce meeting minutes (summary, discussion points, takeaways, and action items) in English.

## Features

- Download transcripts from YouTube using `youtube-transcript-api`.
- Clean and combine transcript snippets into a single text block.
- Build a prompt and call OpenAI's `gpt-4o-mini` model via streaming to produce minutes in Markdown (no code blocks).
- Simple API-key format check and streaming display in notebook cells.

## Contents

- `parlamentai.ipynb` — the main notebook demonstrating transcript retrieval and LLM-powered minutes generation.

## Quick start

1. Open a terminal and create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

2. Install dependencies:

```bash
pip install youtube-transcript-api python-dotenv openai
```

3. Place your OpenAI API key in a `.env` file located in the parent directory of the notebook (the notebook loads env from the parent folder). Example `.env`:

```env
OPENAI_API_KEY=sk-...
```

4. Open the notebook `parlamentai.ipynb` in VS Code or Jupyter and run the cells.

## Environment variables

- `OPENAI_API_KEY` — required. The notebook includes a basic format check to help spot incorrect key values.

## Notes on behavior

- The notebook detects available transcript language tracks and selects the first language it finds (the example video uses Hungarian). The generated minutes are produced in English regardless of the transcript language.
- The notebook streams model output into the notebook display for progressive rendering.

## Security and secret handling

- Do NOT commit `.env` or any API keys to the repository. Clear any notebook outputs containing secrets before committing.
- If a secret was accidentally committed, rotate it immediately and remove it from history.

## Troubleshooting

- If transcript retrieval fails, confirm the `VIDEO_ID` is correct and that the video has a transcript available (auto-generated tracks may be limited).
- If the OpenAI call fails, confirm `OPENAI_API_KEY` is valid and that you have network access. Check the API key prefix and rotate the key if necessary.

## Extending this notebook

- Add language selection or multi-track merging to combine several language tracks.
- Chunk very long transcripts and summarize in sections to avoid token limits.

----

Notebook: parlamentai.ipynb — located alongside this README.

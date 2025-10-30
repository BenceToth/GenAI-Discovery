# Notion LLM Tutor

A small Python-based toolkit and notebook that connects to a Notion page, extracts and cleans its content, and uses that content to improve answers from large language models. Think of it as "chatting with your notes": you ask a technical question and the system uses your Notion page as reference material to give more accurate, context-aware responses.

## Features

- Read and export content from a Notion page (via `notion-exporter` / Notion API)
- Clean exported content (remove images, links, attached file names) to produce compact reference text
- Build an enhanced system prompt that includes Notion content for an LLM
- Query models (OpenAI `gpt-4o-mini` and local Llama via `ollama`) with streaming support
- Example Jupyter notebook demonstrating the complete workflow

## Contents

- `notion_llm-tutor.ipynb` — primary notebook showing imports, environment loading, Notion export, cleaning, prompt assembly and model calls
- `requirements.txt` — Python package dependencies for the notebook
- `README.md` — this file

## Quick start

1. Clone the repository:

```bash
git clone https://github.com/BenceToth/GenAI-Discovery.git
cd GenAI-Discovery/03_Notion_LLM-Tutor
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# For bash / WSL
source .venv/Scripts/activate  # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install --upgrade pip
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add environment variables. Create a `.env` file in the project root (one level above the notebook) or set env vars in your system. Example `.env`:

```env
OPENAI_API_KEY=sk-...
NOTION_API_KEY=ntn_...
NOTION_PAGE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Important: do NOT commit your `.env` or API keys to the repository. See Security notes below.

5. Open the `notion_llm-tutor.ipynb` notebook in VS Code or Jupyter and run the cells. The notebook demonstrates how to:
   - load env variables using `python-dotenv`
   - export a Notion page using `NotionExporter`
   - clean the exported content with regex-based helper `remove_images_links_files`
   - assemble a system prompt with reference material
   - query OpenAI (streaming) or Llama via `ollama`

## Usage examples

- Run the notebook in VS Code: open the notebook file and run cells interactively.
- In the notebook, you'll be prompted to enter a question (or you can modify the `question` variable). The notebook prints the system prompt length (useful when debugging prompt/truncation issues).

## Environment variables

- `OPENAI_API_KEY` — OpenAI API key (keep secret).
- `NOTION_API_KEY` — Notion integration token.
- `NOTION_PAGE_ID` — Notion page ID to export (UUID format: 8-4-4-4-12 with dashes).
- Optionally: `MODEL_GPT` and `MODEL_LLAMA` are set in the notebook for convenience.

## Security and secret handling

- Never hardcode API keys in notebooks or commit them to git. If the key appears anywhere in the git history or in notebook outputs, GitHub's secret scanning can reject pushes.

- If a secret was committed, remove it from the repository history before pushing. Recommended tools:
  - BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/
  - `git filter-repo` (modern and flexible): https://github.com/newren/git-filter-repo

Example (using BFG) to remove a secret string from history:

```bash
# Make a bare clone first
git clone --mirror https://github.com/USERNAME/REPO.git
cd REPO.git
# Replace SECRET with the actual secret value
bfg --replace-text passwords.txt
# Or to remove a single secret literal
bfg --delete-files secret_filename
# Then follow BFG instructions to push the cleaned repo
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

- If GitHub secret scanning flagged and blocked your push, consider rotating the exposed key immediately and follow GitHub's unblock flow only if you're certain the secret has been revoked.

- For notebooks specifically, outputs may contain secrets (because printing variables writes them into the notebook JSON). Clear outputs before committing. See "Clearing notebook outputs" below.

## Clearing notebook outputs

- In VS Code: right-click the cell and choose "Clear Output" (or use the notebook context menu: "Clear All Outputs").
- Programmatic CLI: use `nbconvert` to clear outputs in-place:

```bash
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notion_llm-tutor.ipynb
```

Do this before committing/pushing if you've ever printed sensitive values.

## Troubleshooting

- GitHub rejects push due to secret scanning: check the repository security alerts page and follow the guidance to remove secrets or rotate them.
- Notion export failing: confirm `NOTION_API_KEY` has access to the page or workspace and the `NOTION_PAGE_ID` is correct.
- Long prompts/truncation: if your Notion page is big, consider summarizing or selecting relevant sections before adding to the system prompt. You can also chunk content and use retrieval/embedding approaches for larger corpora.

## Extending this project

- Add a retrieval step: embed Notion blocks and use semantic search to pick the most relevant passages for each question.
- Add caching of Notion exports to avoid hitting rate limits.
- Improve sanitization and formatting of exported blocks (e.g., preserve code blocks while removing images).
- Add a UI interface

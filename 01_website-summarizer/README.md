# Website Summarizer

AI-powered website content summarization with multiple implementation approaches. Choose between functional, OOP, or command-line versions.

## Quick Start

1. **Setup:**
   ```bash
   pip install -r requirements.txt
   # For DeepSeek
   ollama pull deepseek-r1:1.5b && ollama serve
   # OR for OpenAI
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

2. **Use:**
   ```bash
   # Command line
   python3 website_summarizer.py https://cnn.com
   
   # Jupyter notebook
   jupyter lab website-summarizer_basic.ipynb
   jupyter lab website-summarizer.ipynb
   ```

## Files & Implementations

| File | Approach | Best For | Features |
|------|----------|----------|----------|
| `website-summarizer_basic.ipynb` | **Functional** | Learning, quick prototyping | OpenAI/Ollama support, simple setup |
| `website-summarizer.ipynb` | **Object-Oriented** | Production, maintainability | DeepSeek thinking filter, clean architecture |
| `website_summarizer.py` | **Command-Line** | Automation, scripting | CLI args, batch processing, file output |

### Implementation Differences

**Basic Implementation:**
- ✅ Functions-based approach
- ✅ OpenAI API + Ollama compatibility  
- ✅ Simple `.env` setup
- ✅ Beginner-friendly
- ❌ No thinking process filtering

**OOP Implementation:**
- ✅ Class-based architecture
- ✅ DeepSeek thinking process filtering
- ✅ Better error handling
- ✅ Extensible design
- ❌ DeepSeek/Ollama only

**Command-Line Tool:**
- ✅ Terminal automation ready
- ✅ Advanced CLI options
- ✅ File output capabilities
- ✅ Verbose debugging modes
- ❌ No interactive interface

## Dependencies

`requirements.txt`: `requests`, `beautifulsoup4`, `openai`, `python-dotenv`

## Usage Examples

```bash
# CLI with advanced options
python3 website_summarizer.py https://reuters.com --verbose --output news.md

# Basic notebook (OpenAI)
display_summary("https://bbc.com")

# OOP notebook (DeepSeek)
summarizer = WebsiteSummarizer(API, MODEL, HEADERS)
summarizer.display("https://bbc.com")
```

Choose the implementation that best fits your needs: **Basic** for learning, **OOP** for production, **CLI** for automation.

---
*Repository: [BenceToth/GenAI-Discovery](https://github.com/BenceToth/GenAI-Discovery)*
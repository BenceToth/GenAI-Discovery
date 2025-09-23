#!/usr/bin/env python3
"""
Website Summarizer - Terminal Script
OOP-Driven Website summarizer using DeepSeek via Ollama with thinking process filtering.

Usage:
    python website_summarizer.py <url> [options]
    
Examples:
    python website_summarizer.py https://cnn.com
    python website_summarizer.py https://cnn.com --thinking
    python website_summarizer.py https://cnn.com --model llama3.2
    python website_summarizer.py https://cnn.com --output summary.md
"""

import argparse
import sys
import re
import requests
from bs4 import BeautifulSoup
import warnings

# Disable warnings (including SSL warnings)
warnings.filterwarnings('ignore')

# Constants
DEFAULT_API = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "deepseek-r1:1.5b"
DEFAULT_HEADERS = {"Content-Type": "application/json"}


class WebsiteSummarizer:
    """Website summarizer using DeepSeek via Ollama with thinking process filtering."""
    
    def __init__(self, api_url=DEFAULT_API, model=DEFAULT_MODEL, headers=DEFAULT_HEADERS):
        self.api_url = api_url
        self.model = model
        self.headers = headers
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    
    def _filter_thinking(self, text):
        """Remove DeepSeek's <think> tags."""
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
        return cleaned if cleaned else text
    
    def _fetch_website(self, url):
        """Fetch and parse website content."""
        try:
            response = requests.get(url, headers={"User-Agent": self.user_agent}, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No title"
            
            # Remove unwanted elements
            for tag in soup(["script", "style", "img", "input"]):
                tag.decompose()
            
            text = soup.get_text(separator="\n", strip=True)
            return title, text
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch website: {e}")
        except Exception as e:
            raise Exception(f"Error parsing website: {e}")
    
    def summarize(self, url, show_thinking=False, verbose=False):
        """Summarize a website."""
        try:
            if verbose:
                print(f"🌐 Fetching: {url}")
                print(f"🤖 Using model: {self.model}")
                print(f"🔗 API endpoint: {self.api_url}")
                print("📝 Generating summary...")
            
            title, content = self._fetch_website(url)
            
            if verbose:
                print(f"📄 Title: {title}")
                print(f"📃 Content preview (first 500 chars): {content[:500]}...")
                print(f"📏 Total content length: {len(content)} characters")
            
            messages = [
                {"role": "system", "content": """You are a precise content analyzer. ONLY summarize what is actually present in the provided website content. 
                DO NOT make up, infer, or hallucinate any information not explicitly stated in the content.
                If the content is minimal or unclear, state that clearly.
                Provide exact quotes from the content when possible.
                If there are no specific articles or news items, say so."""},
                {"role": "user", "content": f"Website: {title}\n\nContent:\n{content}"}
            ]
            
            payload = {"model": self.model, "messages": messages, "stream": False}
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()['message']['content']
            return result if show_thinking else self._filter_thinking(result)
            
        except Exception as e:
            raise Exception(f"Failed to summarize website: {e}")


def main():
    """Main function to handle command line arguments and execute summarization."""
    parser = argparse.ArgumentParser(
        description="Summarize website content using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://cnn.com
  %(prog)s https://cnn.com --thinking
  %(prog)s https://cnn.com --model llama3.2
  %(prog)s https://cnn.com --output summary.md
        """
    )
    
    parser.add_argument('url', help='URL of the website to summarize')
    parser.add_argument('--thinking', action='store_true', 
                       help='Show AI thinking process (for debugging)')
    parser.add_argument('--model', default=DEFAULT_MODEL,
                       help=f'AI model to use (default: {DEFAULT_MODEL})')
    parser.add_argument('--api', default=DEFAULT_API,
                       help=f'API endpoint URL (default: {DEFAULT_API})')
    parser.add_argument('--output', '-o', 
                       help='Output file to save the summary (optional)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.verbose:
            print(f"🌐 Fetching: {args.url}")
            print(f"🤖 Using model: {args.model}")
            print(f"🔗 API endpoint: {args.api}")
        
        # Create summarizer instance
        summarizer = WebsiteSummarizer(api_url=args.api, model=args.model)
        
        if args.verbose:
            print("📝 Generating summary...")
        
        # Generate summary
        summary = summarizer.summarize(args.url, show_thinking=args.thinking, verbose=args.verbose)
        
        # Output results
        if args.output:
            # Save to file
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"✅ Summary saved to: {args.output}")
            if args.verbose:
                print(f"📊 Summary length: {len(summary)} characters")
        else:
            # Print to terminal
            print("="*60)
            print("WEBSITE SUMMARY")
            print("="*60)
            print(summary)
            print("="*60)
            if args.verbose:
                print(f"📊 Summary length: {len(summary)} characters")
    
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
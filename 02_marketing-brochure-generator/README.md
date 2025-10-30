# Marketing Brochure Generator

An AI-powered tool that automatically creates professional marketing brochures for companies by analyzing their websites.

## 🎯 Business Challenge

Create a product that builds a professional brochure for a company to be used for:
- **Prospective clients** - showcasing products and services
- **Investors** - highlighting growth potential and opportunities
- **Potential recruits** - demonstrating company culture and career opportunities

## 📋 Requirements

- Company name
- Primary website URL
- OpenAI API key

## 🚀 How It Works

The system uses a multi-step AI workflow:

1. **Website Scraping**: Extracts content from the main website using BeautifulSoup
2. **Link Analysis**: Uses GPT-4o-mini to identify relevant pages (About, Careers, Company info)
3. **Content Aggregation**: Scrapes identified relevant pages for comprehensive company information
4. **Brochure Generation**: Creates a structured, professional brochure using all gathered information

## 🛠️ Technical Implementation

### Multi-Shot Prompting
- Uses multiple examples to improve AI understanding
- Ensures consistent JSON formatting for link extraction
- Better handling of various website structures

### Structured Output Format
The generated brochure follows a professional format with sections:
- 🏢 Company Overview
- 🎯 Mission & Vision  
- 💼 Products & Services
- 👥 Leadership & Team
- 🌟 Why Choose Us
- 💰 Investment Highlights
- 🚀 Career Opportunities
- 📈 Company Growth & Future
- 📞 Contact Information

### Features
- **Streaming Output**: Real-time typewriter animation for better UX
- **Error Handling**: Graceful fallbacks for missing information
- **Customizable Tone**: Switch between professional and humorous styles
- **Content Truncation**: Handles large websites efficiently

## 📁 Files

- `brochure-generator.ipynb` - Main Jupyter notebook with complete implementation
- `README.md` - This documentation file
- `requirements.txt` - The packages used for the code.

## 🔧 Setup

1. Install required dependencies:
   ```bash
   pip install openai beautifulsoup4 requests python-dotenv
   ```
   or
   ```bash
    pip install -r requirements.txt
   ```

2. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Run the Jupyter notebook and execute the cells

## 📖 Usage Example

```python
# Create a brochure for any company
create_brochure("HuggingFace", "https://huggingface.co")

# Or use streaming for real-time output
stream_brochure("HuggingFace", "https://huggingface.co")
```

## 🎨 Customization

### Professional Tone (Default)
```python
system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website and creates a professional brochure..."
```

### Humorous Tone (Alternative)
```python
system_prompt = "You are an assistant that creates hilarious, entertaining, and witty brochures about companies while still being informative..."
```

## 🔍 Key Components

### Website Class
- Handles web scraping with proper headers
- Extracts text content and links
- Removes irrelevant elements (scripts, styles, images)

### Link Extraction
- Uses AI to identify relevant company pages
- Converts relative URLs to absolute URLs
- Filters out privacy/terms pages

### Content Processing
- Aggregates information from multiple pages
- Handles content truncation for API limits
- Maintains context across different page types

## 🚧 Limitations

- Requires websites to be publicly accessible
- Content quality depends on website structure
- API rate limits may apply for large-scale usage
- Some websites may block automated scraping

## 🔮 Future Enhancements

- Multi-language support
- PDF export functionality
- Custom branding options
- Integration with CRM systems
- Batch processing for multiple companies
- Enhanced error handling and retry logic
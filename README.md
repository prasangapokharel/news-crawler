# news-crawler

> AI-powered news crawler with a RAG (Retrieval-Augmented Generation) pipeline.  
> Scrapes, processes and summarises news articles using large language models.

## Features

- Automated news scraping from multiple sources
- RAG pipeline for intelligent summarisation
- Alert system for breaking news
- Modular architecture (core / rag / alert)
- Easy to extend with new sources

## Project Structure

```
news-crawler/
├── core/          # Scraping engine
├── rag/           # RAG pipeline & LLM integration
├── alert/         # Notification system
├── testing/       # Test suite
├── docs/          # Documentation
├── main.py        # Entry point
└── requirements.txt
```

## Getting Started

```bash
git clone https://github.com/prasangapokharel/news-crawler.git
cd news-crawler
pip install -r requirements.txt
cp .env.example .env   # Add your API keys
python main.py
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
LLM_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

## License

MIT License — © 2025 Prasanga Pokharel

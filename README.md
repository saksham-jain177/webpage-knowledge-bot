# Webpage Knowledge Bot

A versatile chatbot that scrapes web content, creates a knowledge base, and answers questions using LangChain and Google's Gemini model.

## Features
- Scrapes and processes webpage content
- Creates vector-based knowledge storage
- Answers questions about webpage content
- Provides time-based information
- Estimates content-based durations
- Command-line interface for interaction

## Prerequisites
- Python 3.8+
- OpenRouter API key from [openrouter.ai](https://openrouter.ai)

## Setup

1. Clone the repository and install dependencies:
```bash
git clone https://github.com/saksham-jain177/webpage-knowledge-bot.git
cd webpage-knowledge-bot
pip install -r requirements.txt
```

1. Create a `.env` file in the project root with your API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Running the Bot

Execute these scripts in order:

1. Load webpage data:
```bash
python data_loader.py
```

2. Create vector store:
```bash
python vector_store.py
```

3. Start the bot API:
```bash
python chatbot_api.py
```

4. In a new terminal, run the chat interface:
```bash
python test_chatbot.py
```

## Example Questions
- "What topics are covered in this webpage?"
- "How long is the content duration?"
- "What is the current time?"
- "What time is it in IST?"

# TranslateLLM

A Python service that combines text translation with LLM processing, allowing for seamless translation of text and processing through a local LLM.

## Features

- Text translation using `googletrans`
- Local LLM integration using Ollama
- Configurable via `config.ini`
- Environment variables support
- Comprehensive error handling
- Extensive logging
- Unit testing support
- Docker support

## Project Structure

```
translate-llm/
├── src/                    # Source code
│   ├── config/            # Configuration management
│   ├── services/          # Core services (translation, LLM)
│   └── translate_llm.py   # Main service class
├── tests/                 # Unit tests
├── config.ini            # Configuration file
├── .env                  # Environment variables
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
├── main.py             # Example usage
└── README.md           # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/translate-llm.git
cd translate-llm
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env` and set your environment variables:
```env
LLM_API_KEY=your_api_key_here
TRANSLATION_API_KEY=your_translation_api_key_here
LOG_LEVEL=INFO
```

2. Adjust `config.ini` settings as needed:
```ini
[llm]
model = mistral
model_provider = ollama
temperature = 0.0
base_url = http://localhost:11434
max_tokens = 1000

[translation]
source_lang = auto
target_lang = en
use_cache = true
timeout = 5

[logging]
level = INFO
format = %(asctime)s | %(levelname)s | %(name)s | %(message)s
```

## Usage

Basic usage example:

```python
import asyncio
from translate_llm import TranslateLLM

async def main():
    # Initialize service
    service = TranslateLLM()
    
    # Process text
    result = await service.process(
        text="¡Hola! ¿Cómo estás?",
        target_lang="en",
        system_prompt="You are a helpful assistant."
    )
    
    print(f"Original: {result['original_text']}")
    print(f"Translated: {result['translated_text']}")
    print(f"LLM Response: {result['llm_response']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Docker Support

Build the Docker image:
```bash
docker build -t translate-llm .
```

Run the container:
```bash
docker run --env-file .env translate-llm
```

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=src tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Translate2LLM

REST API service that translates text and processes it through a local LLM (Ollama). Auto-detects source language, translates to your target language, and generates LLM responses.

## Features

- **REST API** with FastAPI (Swagger docs included)
- **Auto language detection** and translation (googletrans)
- **Local LLM** integration via Ollama
- **Docker ready** with single command deployment
- **Python package** for direct integration
- Configurable via `config.ini` and environment variables

## Quick Start

**Prerequisites:**
- Python 3.8+
- [Ollama](https://ollama.ai) installed and running
- Pull a model: `ollama pull mistral`

**Install and run:**
```bash
pip install -r requirements.txt
python api.py
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Configuration

Edit `config.ini` to customize:
```ini
[llm]
model = mistral                          # Ollama model name
base_url = http://localhost:11434        # Ollama server URL
temperature = 0.0

[translation]
target_lang = en                         # Default target language
source_lang = auto                       # Auto-detect source
```

Optional `.env` for API keys (googletrans doesn't require one):
```env
LOG_LEVEL=INFO
```

## Usage

### REST API (Recommended)

**Start server:**
```bash
python api.py
# or: uvicorn api:app --reload
```

**Make requests:**
```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "¡Hola! ¿Cómo estás?", "target_lang": "en"}'
```

**Python client:**
```python
import requests

response = requests.post("http://localhost:8000/translate", json={
    "text": "Bonjour le monde!",
    "target_lang": "en",
    "system_prompt": "You are a helpful assistant."
})

result = response.json()
# Returns: original_text, detected_language, translated_text, llm_response
```

**Interactive docs:** `http://localhost:8000/docs`

### Python Package

**Install from GitHub:**
```bash
pip install git+https://github.com/ozmaatuk/translate2llm.git
```

**Or clone and install locally:**
```bash
git clone https://github.com/ozmaatuk/translate2llm.git
cd translate2llm
pip install -e .
```

**Use in code:**
```python
from translate2llm import TranslateLLM

service = TranslateLLM()
result = service.process(text="Hola", target_lang="en")
print(result['llm_response'])
```

### Docker

```bash
docker build -t translate2llm .
docker run -p 8000:8000 translate2llm
```

Access at `http://localhost:8000`

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /translate` - Translate and process text
  - Body: `{"text": "...", "target_lang": "en", "system_prompt": "..."}`
  - Returns: `{"original_text", "detected_language", "translated_text", "llm_response"}`

## Testing

```bash
pytest tests/                           # Run tests
pytest --cov=translate2llm tests/      # With coverage
```

## Project Structure

```
translate2llm/
├── api.py              # FastAPI REST service
├── src/
│   ├── translate2llm.py    # Main service class
│   ├── config/             # Config management
│   └── services/           # Translation & LLM services
├── tests/              # Unit tests
├── config.ini         # Configuration
└── Dockerfile         # Docker setup
```

## License

MIT License
import os
import sys

# Ensure project root is on sys.path so `import src` works when running tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest
from unittest.mock import Mock, patch
from src.services.llm_service import LLMService
from src.services.translation_service import TranslationService

@pytest.fixture
def llm_config():
    """Test configuration fixture."""
    return {
        "model": "mistral",
        "model_provider": "ollama",
        "temperature": 0.0,
        "base_url": "http://localhost:11434",
        "max_tokens": 1000
    }

@pytest.fixture
def mock_chat_model():
    """Mock ChatModel fixture."""
    model = Mock()
    model.invoke.return_value = Mock(content="Test response")
    model.ainvoke.return_value = Mock(content="Test async response")
    return model

@pytest.fixture
def llm_service(llm_config, mock_chat_model):
    """LLMService fixture with mock model."""
    with patch("src.services.llm_service.init_chat_model", return_value=mock_chat_model):
        return LLMService(llm_config)

from src.services.translation_service import TranslationService

@pytest.fixture
def translation_config():
    """Test configuration fixture."""
    return {
        "source_lang": "auto",
        "target_lang": "en",
        "use_cache": True,
        "timeout": 5
    }

@pytest.fixture
def translation_service(translation_config):
    """TranslationService fixture."""
    return TranslationService(translation_config)

@pytest.fixture
def mock_translator():
    """Mock Translator fixture."""
    translator = Mock()
    translator.translate.return_value = Mock(
        text="Hello",
        src="es",
        dest="en"
    )
    translator.detect.return_value = Mock(
        lang="es",
        confidence=0.9
    )
    return translator

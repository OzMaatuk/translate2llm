"""Unit tests for the LLM service."""


import pytest
from src.services.exceptions import LLMError

from unittest.mock import Mock, patch
from langchain.chat_models.base import init_chat_model


class TestLLMService:
    """Test cases for LLMService."""

    def test_init_chat_model_success(self, llm_config):
        """Test successful chat model initialization."""
        with patch('src.services.llm_service.init_chat_model') as mock_init:
            mock_init.return_value = Mock()
            from src.services.llm_service import LLMService
            service = LLMService(llm_config)
            assert service.llm is not None
            mock_init.assert_called_once()

    def test_process_text_success(self, llm_service):
        """Test successful text processing."""
        llm_service.llm.invoke = Mock(return_value=Mock(content="Test async response"))
        response = llm_service.process_text("Hello", "Be helpful")
        assert response == "Test async response"

    def test_process_text_empty(self, llm_service):
        """Test processing empty text."""
        response = llm_service.process_text("")
        assert response == ""

    def test_process_text_error(self, llm_service):
        """Test text processing error handling."""
        llm_service.llm.invoke = Mock(side_effect=Exception("Processing failed"))
        with pytest.raises(LLMError):
            llm_service.process_text("Hello")

    def test_is_available_true(self, llm_service):
        """Test availability check when LLM is available."""
        assert llm_service.is_available() is True

    def test_is_available_false(self, llm_service):
        """Test availability check when LLM is not available."""
        llm_service.llm.invoke.side_effect = Exception("Connection failed")
        assert llm_service.is_available() is False
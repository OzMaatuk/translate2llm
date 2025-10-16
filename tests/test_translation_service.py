"""Unit tests for the translation service."""
import pytest
from unittest.mock import Mock, patch
from src.services.exceptions import TranslationError
from src.services.translation_service import TranslationService

class TestTranslationService:
    """Test cases for TranslationService."""

    def test_init_with_config(self, translation_config):
        """Test service initialization with config."""
        service = TranslationService(translation_config)
        assert service.source_lang == "auto"
        assert service.target_lang == "en"
        assert service.use_cache is True
        # assert service.timeout == 5

    def test_validate_language_valid(self, translation_service):
        """Test language validation with valid code."""
        assert translation_service.validate_language("en") is True
        assert translation_service.validate_language("es") is True
        assert translation_service.validate_language("fr") is True

    def test_validate_language_invalid(self, translation_service):
        """Test language validation with invalid code."""
        assert translation_service.validate_language("xx") is False
        assert translation_service.validate_language("invalid") is False

    def test_translate_empty_text(self, translation_service):
        """Test translation with empty text."""
        assert translation_service.translate("") == ""
        assert translation_service.translate("   ") == "   "

    @patch('googletrans.Translator')
    def test_translate_success(self, mock_translator_class, translation_service):
        """Test successful translation."""
        mock_result = Mock()
        mock_result.text = "Hello"
        mock_result.src = "es"
        mock_result.dest = "en"
        mock_translator_class.return_value.translate.return_value = mock_result
        translation_service.translator = mock_translator_class.return_value
        result = translation_service.translate("¡Hola!", "en", "es")
        assert result == "Hello"

    @patch('googletrans.Translator')
    def test_translate_error(self, mock_translator_class, translation_service):
        """Test translation error handling."""
        mock_translator_class.return_value.translate.side_effect = Exception("Translation failed")
        translation_service.translator = mock_translator_class.return_value
        with pytest.raises(TranslationError):
            translation_service.translate("¡Hola!", "en", "es")

    @patch('googletrans.Translator')
    def test_detect_language_success(self, mock_translator_class, translation_service):
        """Test successful language detection."""
        mock_result = Mock()
        mock_result.lang = "es"
        mock_result.confidence = 0.9
        mock_translator_class.return_value.detect.side_effect = lambda *a, **kw: mock_result
        translation_service.translator = mock_translator_class.return_value
        result = translation_service.detect_language("¡Hola!")
        assert result == "es"

    @patch('googletrans.Translator')
    def test_detect_language_error(self, mock_translator_class, translation_service):
        """Test language detection error handling."""
        mock_translator_class.return_value.detect.side_effect = Exception("Detection failed")
        translation_service.translator = mock_translator_class.return_value
        with pytest.raises(TranslationError):
            translation_service.detect_language("¡Hola!")
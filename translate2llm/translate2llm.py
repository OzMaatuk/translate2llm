"""Main application class for text translation and LLM processing."""
import logging
from typing import Dict, Optional
from .config.config_manager import Config
from .services.translation_service import TranslationService
from .services.llm_service import LLMService
from .services.exceptions import TranslationError, LLMError

logger = logging.getLogger(__name__)

class TranslateLLM:
    """Main class for handling text translation and LLM processing."""

    def __init__(self, config_path: str = "config.ini"):
        """
        Initialize the TranslateLLM service.
        
        Args:
            config_path: Path to the configuration file
        """
        logger.info("Initializing TranslateLLM service")
        
        # Initialize configuration
        self.config = Config(config_path)
        self.config.setup_logging()
        
        # Initialize services
        self.translation_service = TranslationService(self.config.get_translation_config())
        self.llm_service = LLMService(self.config.get_llm_config())
        
        logger.debug("TranslateLLM service initialized successfully")

    def process(self, text: str, target_lang: Optional[str] = None, 
                source_lang: Optional[str] = None,
                system_prompt: Optional[str] = None) -> Dict:
        """
        Process text through translation and LLM.
        
        Args:
            text: Input text to process
            target_lang: Target language for translation
            source_lang: Source language of input text
            system_prompt: Optional system prompt for LLM
        
        Returns:
            Dict containing:
                - original_text: Original input text
                - detected_language: Detected source language
                - translated_text: Translated text
                - llm_response: LLM response to translated text
                
        Raises:
            TranslationError: If translation fails
            LLMError: If LLM processing fails
        """
        if not text or not text.strip():
            logger.warning("Empty text provided")
            return {
                "original_text": text,
                "detected_language": None,
                "translated_text": text,
                "llm_response": ""
            }

        try:
            # Detect language if not specified
            detected_lang = (source_lang or 
                           self.translation_service.detect_language(text))
            logger.info(f"Detected language: {detected_lang}")

            # Translate if needed
            translated_text = text
            if ((target_lang and detected_lang != target_lang) or 
                (not target_lang and detected_lang != self.translation_service.target_lang)):
                translated_text = self.translation_service.translate(
                    text,
                    target_lang=target_lang,
                    source_lang=detected_lang
                )
                logger.info("Text translated successfully")

            # Process with LLM
            llm_response = self.llm_service.process_text(
                translated_text,
                system_prompt
            )
            logger.info("LLM processing completed")

            return {
                "original_text": text,
                "detected_language": detected_lang,
                "translated_text": translated_text,
                "llm_response": llm_response
            }

        except TranslationError as e:
            logger.error(f"Translation error: {str(e)}")
            raise
        except LLMError as e:
            logger.error(f"LLM error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
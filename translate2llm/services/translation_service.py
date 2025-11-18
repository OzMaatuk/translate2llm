"""Translation service implementation using googletrans."""
import logging
import asyncio
import inspect
from threading import Thread
from typing import Optional, Dict
from functools import lru_cache
from googletrans import Translator, LANGUAGES
from .exceptions import TranslationError

logger = logging.getLogger(__name__)

class TranslationService:
    """Handles text translation using the googletrans library."""

    def __init__(self, config: Dict):
        """
        Initialize the translation service.
        
        Args:
            config: Configuration dictionary containing translation settings
        """
        logger.info("Initializing TranslationService")
        self.config = config
        self.translator = Translator(timeout=self.config["timeout"])
        self.use_cache = self.config.get("use_cache", True)
        self.source_lang = self.config.get("source_lang", "auto")
        self.target_lang = self.config.get("target_lang", "en")
        # Create a dedicated background event loop to run any awaited operations
        self._loop = asyncio.new_event_loop()
        self._loop_thread = Thread(target=self._run_event_loop, daemon=True)
        self._loop_thread.start()
        
        logger.debug(f"TranslationService configured with: {self.config}")

    def _run_event_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def _resolve_maybe_awaitable(self, value):
        """Resolve value that might be an awaitable to its result synchronously."""
        if inspect.isawaitable(value):
            future = asyncio.run_coroutine_threadsafe(value, self._loop)
            return future.result()
        return value

    def validate_language(self, lang_code: str) -> bool:
        """
        Validate if a language code is supported.
        
        Args:
            lang_code: ISO language code to validate
            
        Returns:
            bool: True if language is supported, False otherwise
        """
        return lang_code in LANGUAGES

    @lru_cache(maxsize=1000)
    def _cached_translate(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        """
        Cached version of the translation function.
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (default: auto-detect)
            
        Returns:
            str: Translated text
            
        Raises:
            TranslationError: If translation fails
        """
        try:
            result = self.translator.translate(
                text, 
                dest=target_lang,
                src=source_lang
            )
            result = self._resolve_maybe_awaitable(result)
            logger.debug(f"Translated text from {source_lang} to {target_lang}")
            return getattr(result, "text", str(result))
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise TranslationError(f"Translation failed: {str(e)}")

    def translate(self, text: str, target_lang: Optional[str] = None, 
                 source_lang: Optional[str] = None) -> str:
        """
        Translate text to the target language.
        
        Args:
            text: Text to translate
            target_lang: Target language code (overrides config)
            source_lang: Source language code (overrides config)
            
        Returns:
            str: Translated text
            
        Raises:
            TranslationError: If translation fails
            ValueError: If language code is invalid
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for translation")
            return text

        target = target_lang or self.target_lang
        source = source_lang or self.source_lang

        # Validate language codes
        if target != "auto" and not self.validate_language(target):
            logger.error(f"Invalid target language code: {target}")
            raise ValueError(f"Invalid target language code: {target}")

        if source != "auto" and not self.validate_language(source):
            logger.error(f"Invalid source language code: {source}")
            raise ValueError(f"Invalid source language code: {source}")

        logger.info(f"Translating text from {source} to {target}")
        
        if self.use_cache:
            return self._cached_translate(text, target, source)
        
        try:
            result = self.translator.translate(text, dest=target, src=source)
            result = self._resolve_maybe_awaitable(result)
            logger.debug(f"Translated text from {source} to {target}")
            return getattr(result, "text", str(result))
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise TranslationError(f"Translation failed: {str(e)}")

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        
        Args:
            text: Text to analyze
            
        Returns:
            str: Detected language code
            
        Raises:
            TranslationError: If language detection fails
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for language detection")
            return "und"  # undefined

        try:
            detection = self.translator.detect(text)
            detection = self._resolve_maybe_awaitable(detection)
            logger.debug(f"Detected language: {str(detection)}")
            return getattr(detection, "lang", str(detection))
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")
            raise TranslationError(f"Language detection failed: {str(e)}")
"""LLM service implementation."""
import logging
from typing import Dict, Optional
from langchain.chat_models.base import init_chat_model, BaseChatModel
from src.constants import DEFAULT_MODEL_NAME, DEFAULT_MODEL_PROVIDER, DEFAULT_MODEL_URL
from src.services.exceptions import LLMError


logger = logging.getLogger(__name__)


class LLMService:
    """Handles interactions with the Language Model."""

    def __init__(self, config: Dict):
        """
        Initialize the LLM service.
        
        Args:
            config: LLM configuration dictionary
        """
        logger.info("Initializing LLMService")
        if config == {}:
            config = {
                "model": DEFAULT_MODEL_NAME,
                "model_provider": DEFAULT_MODEL_PROVIDER,
                "base_url": DEFAULT_MODEL_URL
            }
        self.llm: BaseChatModel = init_chat_model(**config)
        logger.info("LLM model initialized successfully")
        self.config = config
        logger.debug(f"LLMService configured with: {config}")

    def process_text(self, text: str, system_prompt: Optional[str] = None) -> str:
        """
        Process text through the LLM model.
        
        Args:
            text: Text to process
            system_prompt: Optional system prompt to guide the model
            
        Returns:
            str: Model response
            
        Raises:
            LLMError: If text processing fails
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for LLM processing")
            return ""

        try:
            # Prepare the messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": text})

            logger.info("Processing text with LLM")
            response = self.llm.invoke(messages)

            if not response or not hasattr(response, 'content'):
                raise LLMError("Invalid response from LLM")
            return str(response.content)

        except Exception as e:
            logger.error(f"LLM processing error: {str(e)}")
            raise LLMError(f"LLM processing failed: {str(e)}")

    def is_available(self) -> bool:
        """Check if the LLM service is available."""
        try:
            # Try a simple prompt to check availability
            test_response = self.llm.invoke("Test.")
            return bool(test_response and hasattr(test_response, 'content'))
        except Exception as e:
            logger.error(f"LLM availability check failed: {str(e)}")
            return False
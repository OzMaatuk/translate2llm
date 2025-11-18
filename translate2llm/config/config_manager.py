"""Configuration management for the application."""
import os
import logging
import configparser
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

class Config:
    """Manages application configuration from config.ini and environment variables."""

    def __init__(self, config_path: str = "config.ini"):
        logger.info(f"Initializing configuration from {config_path}")
        self.config = configparser.ConfigParser()
        self.config_path = Path(config_path)
        
        if self.config_path.exists():
            self.config.read(self.config_path)
            logger.debug("Configuration file loaded successfully")
        else:
            logger.warning(f"Configuration file not found at {config_path}")

    def get_llm_config(self) -> Dict:
        """Load LLM configuration."""
        llm_config = {
            "model": self.config.get("llm", "model", fallback="mistral"),
            "model_provider": self.config.get("llm", "model_provider", fallback="ollama"),
            "temperature": self.config.getfloat("llm", "temperature", fallback=0.0),
            "base_url": self.config.get("llm", "base_url", fallback="http://localhost:11434"),
            "max_tokens": self.config.getint("llm", "max_tokens", fallback=1000),
            "api_key": os.getenv("LLM_API_KEY")
        }
        logger.debug(f"Loaded LLM config: {llm_config}")
        return llm_config

    def get_translation_config(self) -> Dict:
        """Load translation configuration."""
        translation_config = {
            "source_lang": self.config.get("translation", "source_lang", fallback="auto"),
            "target_lang": self.config.get("translation", "target_lang", fallback="en"),
            "use_cache": self.config.getboolean("translation", "use_cache", fallback=True),
            "timeout": self.config.getint("translation", "timeout", fallback=5),
            "api_key": os.getenv("TRANSLATION_API_KEY")
        }
        logger.debug(f"Loaded translation config: {translation_config}")
        return translation_config

    def setup_logging(self) -> None:
        """Configure logging based on configuration."""
        log_level = os.getenv("LOG_LEVEL") or self.config.get("logging", "level", fallback="INFO")
        log_format = self.config.get("logging", "format", 
                                   fallback="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format
        )
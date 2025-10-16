prompt.md

as helpful software engineer, you should implement simple python backend service for:
translating text, send it to llm, and return the response.

translation should use free translation api like googletrans

llm should be local and set following the next example:

import logging
import re
from typing import Union
from langchain.chat_models.base import init_chat_model, BaseChatModel
from src.constants.constants import Constants
from langchain_core.messages import BaseMessage


logger = logging.getLogger(__name__)

class DescriptionMatcher:
    """Matches job descriptions using various methods."""

    def __init__(self, method: str = Constants.DEFAULT_MATCHING_METHOD, threshold: int = Constants.DEFAULT_THRESHOLD, llm_config: dict = {}, prompt_file: str = Constants.DEFAULT_PROMPT_FILE):
        logger.info(f"Initializing DescriptionMatcher with method: {method}")
        logger.debug(f"Using threshold: {threshold}, llm_config: {llm_config}")
        self.method = method
        self.threshold = threshold

        with open(prompt_file, 'r') as file:
            self.prompt = file.read()
        
        self.llm : Union[BaseChatModel, None] = None
        if self.method == "llm":
            logger.debug("Initializing LLM model")
            if llm_config == {}:
                llm_config = {
                    "model": Constants.DEFAULT_MODEL_NAME,
                    "model_provider": Constants.DEFAULT_MODEL_PROVIDER,
                    "base_url": Constants.DEFAULT_MODEL_URL
                }
            self.llm = init_chat_model(**llm_config)
            logger.info("LLM model initialized successfully")

    def matches(self, job_description: str, user_description: str) -> bool:
        logger.debug("DescriptionMatcher.matches")
        
        if not isinstance(job_description, str) or not isinstance(user_description, str) or not job_description.strip() or not user_description.strip():
            raise ValueError("Job descriptions must be strings and cannot be empty")
        
        if self.llm is not None:
            self.prompt = self.prompt.format(job_description=job_description, user_description=user_description)
            logger.debug(f"LLM prompt: {self.prompt}")
            response = self.llm.invoke(self.prompt)
            logger.debug(f"LLM Response: {response}")
            response = str(response.content) if hasattr(response, 'content') else str(response)
            logger.debug(f"LLM Extracted Response: {response}")
            try:
                match = re.search(r'\d+', response)
                if match:
                    score = int(match.group())
                else:
                    raise ValueError("No number found in string") 
            except Exception:
                logger.error(f"Could not parse score from LLM response: {response}")
                return False
            logger.debug(f"Generated score: {score}")
            logger.debug(f"Check if score >= self.threshold: {score} >= {self.threshold}")
            return score >= self.threshold
        elif self.method == "fuzz":
            raise NotImplementedError("Fuzzy matching implementation was removed.")
        else:
            logger.error(f"Invalid matching method in config file: {self.method}")
            raise ValueError(f"Invalid matching method in config file: {self.method}")  

everything shoudl be configurable via config.ini

for api keys use dotenv

keep on all relevant design patterns and coding best practices especially a good python project structure

dont forget error handling, logging, unit testing, readme, requirements.txt, dockerfile

carefully choose libraries


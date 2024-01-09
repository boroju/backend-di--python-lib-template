import logging
from abc import ABC, abstractmethod
from pylibtemplate.config.log.logger import get_logger

from typing import List, Dict


class BaseAssistant(ABC):
    """Abstract base class for defining a BaseAssistant: One answer only."""

    log: logging.Logger = get_logger("BaseAssistant", level=logging.INFO)

    @abstractmethod
    def converse(self, prompt: str, temperature: float) -> str:
        """Preprocesses the conversation before sending it to the assistant service."""
        pass

    @abstractmethod
    def _preprocess_response(self, response: List[Dict]) -> str:
        """Preprocesses the response from the assistant service."""
        pass

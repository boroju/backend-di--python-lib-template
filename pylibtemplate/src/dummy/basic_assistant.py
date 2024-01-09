import string
import random
import time
from pylibtemplate.src.dummy.base import BaseAssistant

from typing import List, Dict


class DummyBasicAssistant(BaseAssistant):
    """Dummy BasicAssistant responding random strings."""

    def _preprocess_response(self, response: List[Dict]) -> str:
        pass

    def converse(self, prompt: str, temperature: float) -> str:
        time.sleep(0.5)
        return "".join(random.choices(string.ascii_letters, k=10))

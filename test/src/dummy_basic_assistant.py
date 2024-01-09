import unittest
from pylibtemplate.config.log.logger import log
from pylibtemplate.src.dummy.basic_assistant import DummyBasicAssistant


class TestDummyBasicAssistant(unittest.TestCase):
    @log
    def test_converse_returns_non_empty_string(self, log):
        # Create an instance of DummyBasicAssistant
        assistant = DummyBasicAssistant()

        # Perform a simulated conversation with the assistant
        prompt = "Test prompt"
        temperature = 0.8
        response = assistant.converse(prompt, temperature)

        # Verify that the response is a non-empty string
        self.assertIsInstance(response, str)
        self.assertTrue(response)

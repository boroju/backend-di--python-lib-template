import logging
import unittest
from logging import Logger

from pylibtemplate.config.log.logger import log


class TestLogger(unittest.TestCase):
    def test_logger_function(self):
        @log
        def my_function(self: unittest.TestCase, log: Logger):
            log.debug("Custom log test")
            self.assertIsInstance(log, logging.Logger)
            self.assertTrue(log.hasHandlers())

        my_function(self)

    def test_logger_function_levels(self):
        @log(level=logging.CRITICAL)
        def my_function(self: unittest.TestCase, log: Logger):
            log.debug("Custom critical log test")
            self.assertIsInstance(log, logging.Logger)
            self.assertEqual(log.level, logging.CRITICAL)

        my_function(self)

    def test_logger_class(self):
        @log
        class MyClass:
            pass

        self.assertIsInstance(MyClass.log, logging.Logger)
        self.assertTrue(MyClass.log.hasHandlers())

    def test_logger_class_levels(self):
        @log(level=logging.DEBUG)
        class MyClass:
            pass

        self.assertIsInstance(MyClass.log, logging.Logger)
        self.assertEqual(MyClass.log.level, logging.DEBUG)

    def test_logger_no_duplicate(self):
        @log(level=logging.DEBUG)
        class MyClass3:
            pass

        @log(level=logging.CRITICAL)
        class MyClass:
            pass

        self.assertIsInstance(MyClass.log, logging.Logger)
        self.assertEqual(MyClass.log.level, logging.CRITICAL)

    def test_logger_no_duplicate_overload(self):
        @log(level=logging.CRITICAL)
        @log(level=logging.DEBUG)
        class MyClass:
            pass

        self.assertIsInstance(MyClass.log, logging.Logger)
        self.assertEqual(MyClass.log.level, logging.CRITICAL)

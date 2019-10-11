import unittest
from unittest.mock import patch, Mock

import sys

from src.masonite.interfaces import Interface
from src.masonite.interfaces.exceptions import InterfaceException


class ConcreteInterface(Interface):

    def auth(self, var1, var2):
        pass


class ConcreteAnnotationInterface(Interface):

    def auth(self, var1, var2: str):
        pass


class ConcreteClassWithCorrectMethods(ConcreteInterface):

    test_attribute = 'Joe'

    def auth(self, var1, var2):
        pass

    def username(self):
        return 'Joe'


class ConcreteClassWithInCorrectSignature(ConcreteInterface):

    def auth(self, var1):
        pass


class ConcreteClassWithTooMuchSignature(ConcreteInterface):

    def auth(self, var1, var2, var3):
        pass


class ConcreteClassWithIncorrectAnnotation(ConcreteAnnotationInterface):

    def auth(self, var1, var2):
        pass


class ConcreteClassWithCorrectAnnotation(ConcreteAnnotationInterface):

    def auth(self, var1, var2: str):
        pass


class TestInterface(unittest.TestCase):

    def test_interface_builds_class(self):
        ConcreteClassWithCorrectMethods()

    def test_interface_throws_exception_on_too_little_signature(self):

        with self.assertRaises(InterfaceException):
            ConcreteClassWithInCorrectSignature()

    def test_interface_throws_exception_on_too_much_signature(self):

        with self.assertRaises(InterfaceException):
            ConcreteClassWithTooMuchSignature()

    def test_interface_can_build_with_correct_annotation(self):

        ConcreteClassWithCorrectAnnotation()

    def test_interface_can_build_with_incorrect_annotation(self):

        with self.assertRaises(InterfaceException):
            ConcreteClassWithIncorrectAnnotation()

    def test_interface_can_use_methods_after_checks(self):

        self.assertEqual(ConcreteClassWithCorrectMethods().username(), 'Joe')

    def test_interface_can_use_attribute_after_checks(self):

        self.assertEqual(ConcreteClassWithCorrectMethods().test_attribute, 'Joe')

    def test_interface_with_checks_disabled(self):
        """
        Test that interface checks are not done when interfaces is disabled.
        No exceptions should occur.
        """
        env = patch.dict('os.environ', {'ENABLE_INTERFACES': 'FALSE'})
        with env:
            ConcreteClassWithIncorrectAnnotation()
            ConcreteClassWithCorrectAnnotation()

    def test_interface_with_checks_enabled(self):
        """Test that interface checks are done when interfaces is enabled."""
        env = patch.dict('os.environ', {'ENABLE_INTERFACES': 'TRUE'})
        with env:
            with self.assertRaises(InterfaceException):
                ConcreteClassWithIncorrectAnnotation()
            ConcreteClassWithCorrectAnnotation()

    def test_interface_with_masonite_debug_on(self):
        """Test that interface checks are done when Masonite DEBUG is on."""
        mock_config = Mock()
        mock_config.application = Mock()
        mock_config.application.DEBUG = True
        sys.modules["config"] = mock_config
        with self.assertRaises(InterfaceException):
            ConcreteClassWithIncorrectAnnotation()

    def test_interface_with_masonite_debug_off(self):
        """Test that interface checks are not done when Masonite DEBUG is off."""
        mock_config = Mock()
        mock_config.application = Mock()
        mock_config.application.DEBUG = False
        sys.modules["config"] = mock_config
        ConcreteClassWithIncorrectAnnotation()

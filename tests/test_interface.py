import unittest
from src.masonite.interfaces import Interface
from src.masonite.interfaces.exceptions import InterfaceException


class ConcreteInterface(Interface):

    def auth(self, var1, var2):
        pass


class ConcreteAnnotationInterface(Interface):

    def auth(self, var1, var2: str):
        pass


class ConcreteClassWithCorrectMethods(ConcreteInterface):

    def auth(self, var1, var2):
        pass


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

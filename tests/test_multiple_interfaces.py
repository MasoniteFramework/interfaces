import unittest
from src.masonite.interfaces import Interface
from src.masonite.interfaces.exceptions import InterfaceException


class OneInterface(Interface):

    def auth(self):
        pass


class TwoInterface(Interface):

    def logout(self):
        pass


class BaseClass:

    def logout(self):
        pass

    def auth(self):
        pass

class ConcreteClass(OneInterface, TwoInterface, BaseClass):
    pass

class BadConcreteClass(OneInterface):
    pass

class TestInterface(unittest.TestCase):

    def test_can_use_multiple_interfaces(self):
        ConcreteClass()
    
    def test_cannot_instantiate_class_with_interfaces_and_no_base_class(self):
        with self.assertRaises(InterfaceException):
            BadConcreteClass()
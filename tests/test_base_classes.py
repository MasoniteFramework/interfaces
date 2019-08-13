import unittest
from src.masonite.interfaces import Interface
from src.masonite.interfaces.exceptions import InterfaceException


class ConcreteBaseClass:

    def auth(self, var1, var2):
        pass

class ConcreteInterface(Interface):

    def logout(self):
        pass

class ConcreteClass(ConcreteBaseClass, ConcreteInterface):
    
    def logout(self):
        pass


class TestBaseClasses(unittest.TestCase):

    def test_can_be_used_with_other_base_classes(self):
        ConcreteClass()

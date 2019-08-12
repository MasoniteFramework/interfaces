# Masonite Interfaces

This package is to add functionality similiar to how other languages implement interfaces.

This will allow you to create an interface class and then all child classes of the interface MUST have the same methods and number of parameters as the interface. 


# Installation

You can pip install this package:

```
$ pip install masonite-interfaces
```

# Getting Started

We can create an interface by creating a simple class that inherits from `masonite.interfaces.Interface`

```python
from masonite.interfaces import Interface

class ConcreteInterface(Interface):

    def user(self, username):
        pass
        
    def logout(self):
        pass
```

Now we can simply use inheritance to add it to the concrete class:

```python
from some.place import ConcreteInterface

class ConcreteImplementation(ConcreteInterface):
    pass
```

This will now keep throwing `InterfaceException`'s until the the concrete class contains the all the methods as the interface as well as
contains all the same parameters as those methods.


```python
from some.place import ConcreteInterface

class ConcreteImplementation(ConcreteInterface):

    def user(self, username):
        # code ...
        
    def logout(self):
        # code ...
```

import inspect
from .exceptions import InterfaceException


class Interface:

    def __new__(cls, *args, **kwargs):
        try:
            from config import application
            if not application.DEBUG:
                try:
                    return super().__new__(cls, *args, **kwargs)
                except TypeError:
                    return super().__new__(cls)
        except ImportError:
            pass

        methods_to_check = {}
        methods_to_check_against = {}
        to_check = {}
        inherited_methods = []

        for base_class in cls.__bases__:
            if not base_class.__name__.endswith('Interface'):
                for key, method in inspect.getmembers(base_class):
                    if not key.startswith('__') and key != 'get_parameters':
                        members = []
                        for param_key, param_value in cls.get_parameters(method):
                            members += [(param_key, param_value)]
                        inherited_methods += [key]
                        # methods_to_check_against.update({key: members})
                continue

            # Get the methods to check from the interface
            for key, method in inspect.getmembers(base_class):
                if not key.startswith('__') and key != 'get_parameters':
                    members = []
                    for param_key, param_value in cls.get_parameters(method):
                        members += [(param_key, param_value)]
                    methods_to_check.update({key: members})

        # Get the methods on the current class
        for key, method in inspect.getmembers(cls):
            if not key.startswith('__') and key != 'get_parameters':
                members = []
                for param_key, param_value in cls.get_parameters(method):
                    members += [(param_key, param_value)]
                methods_to_check_against.update({key: members})


        cls.__to_check__ = methods_to_check_against  
        # Perform Checks
        for method, values in methods_to_check.items():
            # Check the existance
            if method not in cls.__dict__ and (method in cls.__to_check__ and method not in inherited_methods):

                raise InterfaceException(
                    "{}'s {} method must exist".format(cls, method))

            # Check number of arguments
            if len(methods_to_check[method]) is not len(methods_to_check_against[method]):
                raise InterfaceException("{}'s {} method must have {} parameters but it has {}".format(
                    cls, method, len(methods_to_check[method]), len(methods_to_check_against[method])))

            # Check Types
            variable_search_position = 0
            for parameters in methods_to_check[method]:
                is_an_annotation = parameters[1].annotation != parameters[1].empty
                if is_an_annotation:
                    parameter_to_check_against = methods_to_check_against[
                        method][variable_search_position]
                    is_an_annotation = parameter_to_check_against[
                        1].annotation != parameter_to_check_against[1].empty
                    if not is_an_annotation or parameter_to_check_against[1].annotation != parameters[1].annotation:
                        raise InterfaceException("{}'s '{}' argument in {} method must be an annotation of type: {}. Got {}".format(
                            cls, parameter_to_check_against[0], method, parameters[1].annotation, parameter_to_check_against[1].annotation))

                variable_search_position += 1

        try:
            instance = super().__new__(cls, *args, **kwargs)
        except TypeError:
            instance = super().__new__(cls)

        return instance

    def get_parameters(obj):
        try:
            return inspect.signature(obj).parameters.items()
        except TypeError:
            return ()

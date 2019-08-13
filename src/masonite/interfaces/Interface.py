import inspect
from .exceptions import InterfaceException

class Interface:

    def __new__(cls, *args, **kwargs):
        methods_to_check = {}
        methods_to_check_against = {}

        # Compile the Base classes
        for base_classes in cls.__bases__:
            if not base_classes.__name__.endswith('Interface'):
                continue
            
            for key, method in inspect.getmembers(base_classes):
                if not key.startswith('__') and key != 'get_parameters':
                    members = []
                    for param_key, param_value in cls.get_parameters(method):
                        members += [(param_key, param_value)]
                    methods_to_check.update({key: members})

        # Compile current cls
        for key, method in inspect.getmembers(cls):
            if not key.startswith('__') and key != 'get_parameters':
                members = []
                for param_key, param_value in cls.get_parameters(method):
                    members += [(param_key, param_value)]
                methods_to_check_against.update({key: members})

        # Perform Checks
        for method, values in methods_to_check.items():
            # Check the existance
            if method not in cls.__dict__:

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
        instance = super().__new__(cls, *args, **kwargs)
        return instance
    def get_parameters(obj):
        try:
            return inspect.signature(obj).parameters.items()
        except TypeError:
            return ()



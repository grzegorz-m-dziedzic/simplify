import inspect
from functools import total_ordering

def simplify(cls):

    def get_user_defined_functions():
        return (m[0] for m in inspect.getmembers(cls, predicate=inspect.isfunction))

    @total_ordering
    class Wrapped(*cls.__bases__):
        init_args = list(param for param in inspect.signature(cls.__init__).parameters if param != 'self')

        def __init__(self, *args, **kwargs):
            for arg in Wrapped.init_args:
                default = inspect.signature(cls.__init__).parameters[arg].default
                if not isinstance(default, inspect._empty):
                    setattr(self, arg, default)

            for arg, value in zip(Wrapped.init_args, args):
                setattr(self, arg, value)

            for key, val in kwargs.items():
                setattr(self, key, val)

            cls.__init__(self, *args, **kwargs)

        def __lt__(self, other):
            user_method_result = cls.__lt__(self, other)
            if user_method_result is not NotImplemented:
                return user_method_result

            me = tuple(val for _, val in self.__dict__.items())
            other = tuple(val for _, val in other.__dict__.items())
            return me < other

        def __eq__(self, other):
            user_method_result = cls.__eq__(self, other)
            if user_method_result is not NotImplemented:
                return user_method_result

            me = tuple(val for _, val in self.__dict__.items())
            other = tuple(val for _, val in other.__dict__.items())
            return me == other

        def __str__(self):
            if '__str__' in get_user_defined_functions():
                return cls.__str__(self)

            return '<{} ({})>'.format(cls.__name__,
                                      ', '.join('{}:{}'.format(key, val) for key, val in self.__dict__.items()))

        def __repr__(self):
            if '__repr__' in get_user_defined_functions():
                return cls.__repr__(self)

            return self.__str__()

    return Wrapped

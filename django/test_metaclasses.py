import types
from functools import wraps


def print_type(name, object):
    print(name, type(object))


def notify(fn, *args, **kwargs):
    """Function that prints the name of a passed in function, and returns a new function
    encapsulating the behavior of the original function"""

    def fncomposite(*args, **kwargs):
        print("running %s" % fn.__name__)
        rt = fn(*args, **kwargs)
        return rt
    return fncomposite


class Notifies(type):

    def added_by_metaclass(self):
        print('added by metaclass invoked :)')

    def __new__(cls, name, bases, attr, notifies_prefix):
        # decorates each function with notifies decorator
        attr['added_by_metaclass'] = cls.added_by_metaclass
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = notify(value)
        return super().__new__(cls, name, bases, attr)


class BeingLogged(metaclass=Notifies, notifies_prefix='NTFR:'):

    def first_method(self):
        pass

    def second_method(self):
        pass


class PlainClass():

    def first_method(self):
        pass

    def second_method(self):
        pass


def class_decorator(cls):
    class Wrapper(cls):
        def added_by_decorator(self):
            print('added by decorator')
    return Wrapper


DecoratedClass = class_decorator(PlainClass)

instance = DecoratedClass()
instance.first_method()
instance.second_method()
instance.added_by_decorator()

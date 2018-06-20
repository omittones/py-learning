print('__init__ from Module')

from root_module import say_hello_from_root_module
from .main import say_hello_from_module
from . import submodule

__all__ = ['say_hello_from_module', 'submodule']
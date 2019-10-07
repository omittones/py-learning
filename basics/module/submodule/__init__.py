import sys
import os.path

print('__init__ from Submodule')

from .main import say_hello_from_submodule

sys.path.append(os.path.join(sys.path[0], 'third_party'))
import ext_module
# this does not work because when this is run as a script
# then name of the script will be __name__ == '__main__'
# which means this is not a package and you won't be able to relative import from non package
# from . import module

import module

module.say_hello_from_module()
module.say_hello_from_root_module() #root_module is imported in module/__init__.py, and it works because of sys.path

print('contents of module', dir(module))
print('contents of submodule', dir(module.submodule))
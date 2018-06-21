def test_modules():

    #this does not work because when this is run as a script
    #then name of the script will be __name__ == '__main__'
    #which means this is not a package and you won't be able to relative import from non package
    #from . import module

    import module   # will execut inits for module and all submodules of module
    #import module.submodule.main # would also execute __init__ files in all 3 modules

    module.say_hello_from_module()
    module.say_hello_from_root_module() #root_module is imported in module/__init__.py, and it works because of sys.path

    print('contents of module', dir(module))
    print('contents of submodule', dir(module.submodule))

def test_callables():
    class multiplicator():
        def __init__(self, multiplicator):
            self.multiplicator = multiplicator
        def __call__(self, number):
            return self.multiplicator * number
    multiply = multiplicator(10)
    print(multiply(5))  # prints 50  
    print(multiply(10))  # prints 100        
    print(multiplicator.__call__) # class itself is callable
    print(callable(multiplicator)) # yes, it's callable

def test_timeit():
    from timeit import timeit, repeat
    print(timeit("print('from stmt')", "print('from setup')", number = 10)) # runs 'from setup' and then 'from stmt' 10 times
    result = None
    print(timeit(setup='from __main__ import multiply', stmt = 'result = multiply(10) + multiply(5)', number=10)) # run 10 times
    print(result) # not available after timeit
    print(repeat(setup='from __main__ import multiply', stmt = 'result = multiply(10) + multiply(5)', repeat=3, number=10)) # timeit 3 times

def test_conditional():
    result = 1 if True == False else 2 # result will be 2
    print(result)

def test_lambda():
    from random import choices, sample
    items = choices(range(10), k=9) # 9 random numbers, can be same
    print(items)
    items = sample(range(10), k=9) # 9 random numbers, cannot be same
    print(items)   

    # sorted() is actually sorted(iterable, key=None, reverse=False)
    print(sorted(items, reverse=False))
    print(sorted(items, reverse=True))
    print(sorted(items, key = lambda number: number % 2 )) # order even first, then odd later

def test_args():
    def any_nm_args(*args):
        for a in args:
            print(a)
    def at_least_one_arg(arg, *args):
        print(arg)
        any_nm_args(*args)  
    any_nm_args(1,2,3)
    at_least_one_arg(1,2,3)
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

def test_closure():

    def create_adder(): # function factory
        a = 1
        b = 2
        def adder(c): # clojures are created
            return a + b +c
        return adder

    adder = create_adder()
    print(adder(3))
    print(adder.__closure__) # references to clojure variables

def test_decorators():

    def log_name(prefix):
        def decorator(f):
            def log_and_call(*args, **kwargs):
                print(prefix, 'executing', f.__name__)
                value = f(*args, **kwargs)
                print(prefix, 'executed', f.__name__)
                return value
            return log_and_call
        return decorator

    @log_name('Test')
    def simple_add(x, y):
        return x + y

    print(simple_add(1,2)) # decorator is a callable called with function as argument and it returns a callable
    # executing simple_add
    # executed simple_add
    # 3

def test_class_attributes():
    class Person():
        name = 'undefined'
        age = -1
        def __init__(self):
            super().__init__()
        def set_info(self, name, age):
            self.name = name
            self.age = age
        def print_info(self):
            print(self.name, 'aged', self.age)

    p1 = Person()
    p2 = Person()
    p1.print_info()
    p2.print_info()
    p1.set_info('Anton', 123)
    p1.print_info()
    p2.print_info()
    print('Class attr is', Person.name, Person.age)
    Person.name = 'changed'
    p1.print_info()
    p2.print_info()
    print('Class attr is', Person.name, Person.age)
    p2.age += 1
    p1.print_info()
    p2.print_info()
    print('Class attr is', Person.name, Person.age)


def test_static_methods():
    class Math():
        @staticmethod
        def add_numbers(a, b):
            return a + b
        @classmethod
        def create_math(Klass):
            return Klass()

    class AdvancedMath(Math):
        @staticmethod
        def add_numbers(a, b):
            return a + b
        
    print(Math.add_numbers(1,2)) # returns 3, works but
    print(AdvancedMath.add_numbers(1,2)) # this one is better
    print(Math.create_math()) # creates instance of Math
    print(AdvancedMath.create_math()) # creates instance of AdvancedMath because of @classmethod

def test_properties():

    import math

    class Container():
        def __init__(self, width, height, depth):
            self.width = width
            self.height = height
            self.depth = depth

        @property
        def volume(self):
            return self.width * self.height * self.depth

        @volume.setter
        def volume(self, value):   # must be named the same as property
            factor = value / self.volume 
            factor = math.pow(factor, 1.0 / 3.0)
            self.width *= factor
            self.height *= factor
            self.depth *= factor
            #if self.volume != value:
            #    raise AssertionError('Volume mismatch!')
            
    container = Container(1,2,5)
    print(container.volume) # returns 10
    container.volume = 10
    print(container.volume)
    container.volume = 20
    print(container.volume)

def test_decimals():
    from decimal import Decimal
    from fractions import Fraction
    result = Decimal('1.0') * Fraction(1, 3)
    print(result)

def test_decorator_and_self():

    from functools import wraps

    def htmlify(method):
        @wraps(method)
        def decorated(self, *args, **kwargs):
            print(f'<span class="{self.name}">')
            ret = method(self, *args, **kwargs)
            print('</span>')
            return ret
        return decorated
    
    class Person():
        def __init__(self, **kwargs):
            self.name = kwargs.get('name', 'default-name')
        @htmlify
        def say_name(self, greeting):
            print(greeting + ', my name is', self.name)
        def say_name_again(self, greeting):
            print(greeting + ', my name is', self.name)
        def say_name_loudly(self, greeting):
            print(greeting + ', my name is', self.name + '!!!')
        def say_name_to_person(self, person):
            print('Hello', person + ', my name is', self.name)

    # do it normally
    p1 = Person(name='Jorge')
    p1.say_name('Hello')

    # do it manually
    Person.say_name_again = htmlify(Person.say_name_again)
    p1.say_name_again('Hi')

    # do it after you got the object for every object of that class
    p1.__class__.say_name_loudly = htmlify(p1.__class__.say_name_loudly)
    p1.say_name_loudly('Heeeeelllooo')    

    # do it for one object
    p2 = Person(name='Ben')
    decorated = htmlify(p2.__class__.say_name_to_person)
    p2.say_name_to_person = decorated.__get__(p2, p2.__class__)
    p1.say_name_to_person('Ben')
    p2.say_name_to_person('Jorge')

def test_timeit_comprehensions():

    def for_loops():
        numbers = list()
        for i in range(1000):
            if i % 2 != 0:
                numbers.append(i * 2)
        return numbers

    def comprehension():
        return [i * 2 for i in range(1000) if i % 2 != 0]

    import timeit
    print(timeit.timeit(stmt='test()', number = 10000, globals={'test':for_loops}))
    print(timeit.timeit(stmt='test()', number = 10000, globals={'test':comprehension}))

def test_functools():
    import functools
    import operator
    print(list(map(lambda a,b : (a,b), [1,2], [3,4]))) # returns [(1,3),(2,4)]
    print(list(filter(lambda a : a > 3, [1,2,3,4,5]))) # returns [4,5]
    print(functools.reduce(operator.add, [1,2,3]))
    sum = functools.partial(functools.reduce, operator.add)
    print(sum([1,2,3]))

def test_iteration():
    a = 0
    def my_callable():
        nonlocal a  # since python does not have variable definition syntax, this resolves to a = a + 1, and the idiot tries to make 'a' local, which it isn't (so we need nonlocal at the beggining)
        print('called with a ==', a)
        a += 1   # since python does not have variable definition syntax, this resolves to a = a + 1, and the idiot tries to make 'a' local, which it isn't (so we need nonlocal at the beggining)
        return a
    for i in iter(my_callable, 3):
        print('output is', i)

def test_multiple_inheritace():
    from pprint import pprint as pp
    class Base():
        def sum(self, a, b):
            return a + b
    class OnlyInts(Base):
        def sum(self, a, b):
            if not isinstance(a, int) or not isinstance(b, int):
                raise AssertionError('a and b must be ints!')
            return super().sum(a, b)
    class OnlyPositive(Base):
        def sum(self, a, b):
            if a < 0 or b < 0:
                raise AssertionError('a and b must be positive!')
            return super().sum(a, b)
    class OnlyPositiveInts(OnlyInts, OnlyPositive):
        pass

    pp(OnlyPositiveInts.mro())
    pp(super(OnlyInts, OnlyPositiveInts))
    obj = OnlyPositiveInts()
    obj.sum(-1, 1)
    obj.sum(2.1, 3.1)

def test_context_managers():

    def get_context_manager():
        
        class CM:
            def __enter__(self):
                print('from enter')
                return 'returned from CM()'
            def __exit__(self, exc_type, exc_value, exc_traceback):
                print('from exit')
                #return True # to stop propagation of exception
                #if returns None or False, exception is propagated

        print('from context manager')
        return CM()

    with get_context_manager() as something:
        print(something) # something is value return from __enter__

test_multiple_inheritace()
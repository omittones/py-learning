import sys
import time
import Root_Class
import Module
import functools as ft
import numpy as np

print(sys.stdout.encoding)

Root_Class.say_hello()
Module.say_hello()
Module.Submodule.say_hello()
Module.Submodule.ExtModule.say_hello()

def get():
    return [{ 'ime':'ime' + str(i), 'godine':i % 54 } for i in range(0, 1000000)]

times = dict({ 
    'sum(forgenr) time: ':0,
    'sum(foraray) time: ':0,
    'sum(maplamb) time: ':0,
    'reduce(lamb) time: ':0 
})

for i in range(10):

    lista = get()
    start = time.clock()
    print(sum(x['godine'] for x in lista))
    times['sum(forgenr) time: '] += time.clock() - start
    del lista

    lista = get()
    start = time.clock()
    print(sum([x['godine'] for x in lista]))
    times['sum(foraray) time: '] += time.clock() - start
    del lista

    lista = get()
    start = time.clock()
    print(sum(map(lambda x : x['godine'], lista)))
    times['sum(maplamb) time: '] += time.clock() - start
    del lista

    lista = get()
    start = time.clock()
    print(ft.reduce(lambda value, item: value + item['godine'], lista, 0))
    times['reduce(lamb) time: '] += time.clock() - start
    del lista

for (key, value) in times.items():
    times[key] = value / 10
    print(key, value)
import numpy as np
import time
import random
import cy_min_max
from collections import deque

repeat_count = 250
list_size = 825

def custom_min(input):
    min = np.min(data)
    return min

def custom_max(input):
    min = np.max(data)
    return min

data = []
que = deque(maxlen=list_size)
while len(data) < list_size:
    i = random.randint(20000,23000)
    data.append(i)
    que.append(i)


############################################################

before = time.time()
for i in range(0,repeat_count):
    min = custom_min(data)
    max = custom_max(data)

after = time.time()

print(min, max)
print("numpy in python time:", after - before)


############################################################

before = time.time()
for i in range(0,repeat_count):
    min = cy_min_max.np_min(data)
    max = cy_min_max.np_max(data)

after = time.time()

print(min, max)
print("numpy in cython time:", after - before)
before = time.time()


############################################################

for i in range(0,repeat_count):
    min = cy_min_max.def_min(data)
    max = cy_min_max.def_max(data)

after = time.time()

print(min, max)
print("c min max in cython time:", after - before)

############################################################

before = time.time()
for i in range(0,repeat_count):
    min = cy_min_max.c_min_of_array(data)
    max = cy_min_max.c_max_of_array(data)

after = time.time()

print(min, max)
print("c min max(loop in pyx) in cython time:", after - before)

############################################################









print()











############################################################

before = time.time()
for i in range(0,repeat_count):
    min = custom_min(que)
    max = custom_max(que)

after = time.time()

print(min, max)
print("numpy in python time:", after - before)


############################################################

before = time.time()
for i in range(0,repeat_count):
    min = cy_min_max.np_min(que)
    max = cy_min_max.np_max(que)

after = time.time()

print(min, max)
print("numpy in cython time:", after - before)
before = time.time()


############################################################

for i in range(0,repeat_count):
    min = cy_min_max.def_min(que)
    max = cy_min_max.def_max(que)

after = time.time()

print(min, max)
print("c min max in cython time:", after - before)

############################################################

before = time.time()
for i in range(0,repeat_count):
    min = cy_min_max.c_min_of_array(que)
    max = cy_min_max.c_max_of_array(que)

after = time.time()

print(min, max)
print("c min max(loop in pyx) in cython time:", after - before)

############################################################
cdef int c_min(int val1, int val2):
    if val1<val2:
        return val1
    return val2


cdef int c_max(int val1, int val2):
    if val1>val2:
        return val1
    return val2


def min_of_array(input):
    cdef int x
    x = input[0]
    for i in range(1, len(input)):
        x = c_min(x, input[i])
    return x


def max_of_array(input):
    cdef int x
    x = input[0]
    for i in range(1, len(input)):
        x = c_max(x, input[i])
    return x
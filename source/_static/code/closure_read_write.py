def foo(x):
    def read():
        return x
    def write(y):
        nonlocal x
        x += y
        return x
    return read, write

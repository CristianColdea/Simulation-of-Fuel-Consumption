# first list
a = ['a', 'b', 'c']

# second list
b = [2, 3, 4]

# dict from the lists
d = dict(zip(a, b))

# just a function
def f(x1, x2):
    return 9.5 * (x1 + x2)

r = f(d['a'], d['b'])

print(r)

# just a class
class C:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def fc(a, b):
        return 9.5 * (a + b)

rc = C.fc(d['a'], d['b'])

print(rc)
